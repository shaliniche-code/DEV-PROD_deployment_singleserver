pipeline {

       agent any
          stages {
              stage("Git clone") {
                  steps {
                       git branch: 'main', 
                           credentialsId: 'github-ssh', 
                           url: 'git@github.com:shaliniche-code/DEV-PROD_deployment_singleserver.git'
                      }
}
               stage("listing the files") {
                  steps {
                       sh 'ls'
                      }
}
               stage("build image using docker") {
                steps {
                    sh '''
                    docker rmi -f pythonapp || true
                    docker build -t pythonapp .
                    '''
                     }
}
               stage("push to dockerhub") {
                     steps {
                           withCredentials([
                              usernamePassword(
                                   credentialsId: 'dockerhub-creds', 
                                   passwordVariable: 'DOCKER_PASS', 
                                   usernameVariable: 'DOCKER_USERNAME')
                           ]) 

                        {
                            sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USERNAME --password-stdin
                            docker tag pythonapp $DOCKER_USERNAME/pythonapp:latest
                            docker push $DOCKER_USERNAME/pythonapp:latest
                            '''

                         }
}
}
                 stage("Deploy DEV") {
                    steps {
                       sh '''
                       ssh ubuntu@3.109.132.79 "
                        
                        docker pull shalinidocker12/pythonapp:latest

                        docker stop devapp || true
                        docker rm devapp || true

                        docker run -d \
                        --name devapp \
                        -p 5000:5000 \
                        -e APP_ENV=Development \
                        shalinidocker12/pythonapp:latest
                        " 
                        '''
}
}
                      
}
}                     
