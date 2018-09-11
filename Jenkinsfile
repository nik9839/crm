pipeline {
   agent any
   options { disableConcurrentBuilds() }
   stages {
       stage("Build & Publish") {
           when {
               anyOf {
                    branch "master"
                    branch "develop"
               }
           }
           steps {
               checkout scm
               configFileProvider([configFile(fileId: 'f55e8e98-97f9-431d-87f7-3ede06ecf5b1')])
               script {
                   docker.withRegistry("https://veris.azurecr.io/","vj-azure-container-registry") {
                        docker.build("veris.azurecr.io/crm:${BUILD_TAG}").push()
                   }
               }
           }
       }
   }
   post {
        cleanup {
            sh "docker rmi veris.azurecr.io/crm:${BUILD_TAG}"
        }
   }
}
