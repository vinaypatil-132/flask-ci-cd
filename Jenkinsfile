pipeline {
  agent any

  environment {
    IMAGE = "vinu890/flask-ci-cd"   // <-- replace with your Docker Hub username/repo if needed
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Unit Tests') {
      steps {
        sh '''
            python3 -m venv venv
            . venv/bin/activate
            pip install --upgrade pip
            pip install -r requirements.txt
            pytest -q
        '''
      }
    }

    stage('Build Docker') {
      steps {
        script {
          def tag = (env.GIT_COMMIT ?: "local").take(7)
          sh "docker build -t ${IMAGE}:${tag} ."
          env.IMG_TAG = "${IMAGE}:${tag}"
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh '''
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push "$IMG_TAG"
          '''
        }
      }
    }

    stage('Blue-Green Deploy') {
      steps {
        sh '''
          set -euo pipefail

          # create network if missing
          docker network inspect bluegreen_net >/dev/null 2>&1 || docker network create bluegreen_net

          # pull image that was pushed
          docker pull "$IMG_TAG"

          # decide which name is new/old
          if [ "$(docker ps -q -f name=sample-app-blue -f status=running | wc -l)" -gt 0 ]; then
            NEW_NAME=sample-app-green
            OLD_NAME=sample-app-blue
          else
            NEW_NAME=sample-app-blue
            OLD_NAME=sample-app-green
          fi

          echo "Deploying $IMG_TAG as $NEW_NAME (old is $OLD_NAME)"

          # ensure fresh start
          docker rm -f "$NEW_NAME" >/dev/null 2>&1 || true

          # run new container on the bluegreen network (no host port)
          docker run -d --name "$NEW_NAME" --network bluegreen_net "$IMG_TAG"

          # wait for health by using curl image inside same network
          OK=0
          for i in $(seq 1 12); do
            echo "Checking health of $NEW_NAME (attempt $i)..."
            if docker run --rm --network bluegreen_net curlimages/curl:latest -sS "http://$NEW_NAME:5000/health" >/dev/null 2>&1; then
              OK=1
              break
            fi
            sleep 5
          done

          if [ "$OK" -ne 1 ]; then
            echo "Health check failed for $NEW_NAME, removing it."
            docker rm -f "$NEW_NAME" || true
            exit 1
          fi

          # prepare nginx config (proxy to the new container)
          cat > /tmp/nginx_bluegreen.conf <<'NGINXCONF'
events {}
http {
  server {
    listen 80;
    location / {
      proxy_pass http://__UPSTREAM__:5000;
      proxy_set_header Host \$host;
      proxy_set_header X-Real-IP \$remote_addr;
      proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
  }
}
NGINXCONF

          sed -i "s|__UPSTREAM__|$NEW_NAME|" /tmp/nginx_bluegreen.conf

          # restart proxy with new config (expose host:8081 -> container:80)
          docker rm -f sample-nginx >/dev/null 2>&1 || true
          docker run -d --name sample-nginx --network bluegreen_net -p 8081:80 -v /tmp/nginx_bluegreen.conf:/etc/nginx/nginx.conf:ro nginx:alpine

          # safely remove old app container
          docker rm -f "$OLD_NAME" >/dev/null 2>&1 || true

          echo "Deployment complete. App is available at http://localhost:8081/ (proxied to $NEW_NAME)."
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'index.html', allowEmptyArchive: true, fingerprint: true
    }
  }
}
