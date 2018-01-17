pipeline {
    agent {
            docker { image 'python:3.5.1' 
                     args '-u root:root'
                    }
    }
    
    stages {
        stage('build') {
            steps {
                echo 'cloning github repository'
                checkout scm
                echo 'Install project requirements'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test'){
            steps{
                echo 'nosetests test'
            }
        }
    }

    post{
        always{
            archiveArtifacts artifacts:'*', fingerprint:true
        }
    }
}
