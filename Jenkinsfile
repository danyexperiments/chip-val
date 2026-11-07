pipeline {
    agent any

    environment {
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment Setup') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Execute Pytest Suite') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --port=SIMULATED -n 2
                '''
            }
        }
    }

    post {
        always {
            // Archive JUnit XML report for Jenkins test trends
            junit allowEmptyResults: true, testResults: 'reports/result.xml'
            
            // Publish standalone Pytest HTML report
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Pytest Hardware Validation Report'
            ])
        }
    }
}