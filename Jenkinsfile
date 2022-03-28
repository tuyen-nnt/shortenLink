pipeline {
  agent any
  
  stages {
    stage('Build image') {
      steps {
        sh 'docker build -t short_link_dev:2.0 .'
      }
    }

    stage('Delete old container') {
      steps {
        sh 'docker rm -f short_link_dev'
      }
    }

    stage('Run new container') {
      steps {
        sh 'docker run -p 50002:8080 -d --name short_link_dev short_link_dev:2.1'
      }
    }

  }
}
