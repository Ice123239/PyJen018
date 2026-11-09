pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                bat 'py -3 -m py_compile main.py test_main.py'
            }
        }
        stage('Test') {
            steps {
                bat 'py -3 -m unittest -v'
            }
        }
        stage('Deploy') {
            steps {
                bat '(echo 70& echo 1.75) | py -3 main.py'
            }
        }
    }
}
