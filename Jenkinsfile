pipeline {
    agent any
    
    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository using credentialsId
                git branch: 'main', credentialsId: 'jenkin1', url: 'https://github.com/Aditya-jaiswal07972/Math-Based-Captcha.git'
            }
        }
        
        stage('Build and Run Python Script') {
            steps {
                // Navigate to the directory containing your Python script
                dir('blob/main/python-captha.py') {
                    // Install any required dependencies using pip
                    bat 'pip install -r requirements.txt'
                    
                    // Generate the captcha image and run the Python script
                    bat 'python python-captcha.py'
                    
                    // Optionally, capture the output of the script and save it to a file
                    // bat 'python python-captcha.py > output.txt'
                }
            }
        }
    }
}
