pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                bat 'python -m py_compile main.py test_main.py'
            }
        }
        stage('Test') {
            steps {
                bat 'python -m unittest test_main.py'
            }
        }
        stage('Deploy') {
            steps {
                bat 'python main.py'
            }
        }
    }
}