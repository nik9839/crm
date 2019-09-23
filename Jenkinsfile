pipeline {
   agent any
   options { disableConcurrentBuilds() }
   stages {
       stage("Build & Publish") {
           when {
               anyOf {
                    branch "master"
                    branch "develop"
                    branch "crm_demo"
               }
           }
           steps {
               checkout scm
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
