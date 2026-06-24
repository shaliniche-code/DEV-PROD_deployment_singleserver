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
                       ssh ubuntu@172.31.32.205 "
                        
                        docker pull shalinidocker12/pythonapp:latest

                        docker stop devapp || true
                        docker rm -f  devapp || true
                       
                        echo '===== AFTER REMOVE ====='
                        docker ps -a
                        
                        docker run -d \
                        --name devapp \
                        -p 5000:5000 \
                        -e APP_ENV=Development \
                        shalinidocker12/pythonapp:latest
                        
                        echo '===== AFTER RUN ====='
                        docker ps -a
                        " 
                        '''
}
}
                   stage("Health check") {
                    steps {
                        sh '''
                        ssh ubuntu@172.31.32.205 "
                        sleep 10
                        curl -f http://localhost:5000
                        "
                        '''
}
}
                  stage("Approval") {
                    steps {
                        input 'Deploy to production?'
                        }
}


                  stage("PROD Deployment") {
                     steps {
                          sh '''
                          ssh ubuntu@172.31.32.205 "
                          
                          docker pull shalinidocker12/pythonapp:latest
                         
              
                          docker stop prodapp || true
                          docker rm -f  prodapp || true
                     
                          docker run -d \
                          --name prodapp \
                          -p 5001:5000 \
                          -e APP_ENV=PRODUCTION \
                          shalinidocker12/pythonapp:latest
                          "
                          '''
}
}
                      
}
}                     
