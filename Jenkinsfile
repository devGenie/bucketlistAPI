pipeline {
    agent {
            docker { image 'python:3.5.1' 
                     args '-u root:root'
                    }
    }
    
    stages {
        stage('build') {
            steps {
                properties([pipelineTriggers([[$class: 'GitHubPushTrigger'], pollSCM('H/15 * * * *')])])
                echo 'cloning github repository'
                checkout scm
                echo 'Install project requirements'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test'){
            steps{
                sh 'nosetests'
            }
        }
    }
}
