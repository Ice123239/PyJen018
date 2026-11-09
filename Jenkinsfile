pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                bat '"C:/Users/ADMIN/AppData/Local/Python/bin/python.exe" -m py_compile main.py test_main.py'
            }
        }
        stage('Test') {
            steps {
                bat '"C:/Users/ADMIN/AppData/Local/Python/bin/python.exe" -m unittest test_main.py'
            }
        }
        stage('Deploy') {
            steps {
                bat '"C:/Users/ADMIN/AppData/Local/Python/bin/python.exe" main.py'
            }
        }
    }
}