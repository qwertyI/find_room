pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        sh 'python find_room.py'
      }
    }
    stage('release') {
      steps {
        echo 'after find'
      }
    }
  }
}