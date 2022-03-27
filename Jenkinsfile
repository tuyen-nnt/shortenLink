pipeline {
  agent any
  
  stages {
    stage('Build image') {
      steps {
        sh 'docker build -t short_link:2.0 .'
      }
    }

    stage('Delete old container') {
      steps {
        sh 'docker rm -f short_link'
      }
    }

    stage('Run new container') {
      steps {
        sh 'docker run -p 50001:8080 -d --name short_link short_link:2.0'
      }
    }

  }
}
