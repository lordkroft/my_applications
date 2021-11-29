pipeline{
    agent any
    parameters{
        string(defaultValue: 'us-east-2', name: ${AWS_DEFAULT_REGION})
        string(name: ${IMAGE_TAG})
    }

    stages{
        stage("Building image"){
            steps{
                    sh "docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.AWS_DEFAULT_REGION.amazonaws.com/spase-registry:${params.IMAGE_TAG} ." 
                }
            }
        stage("Pushing to ECR"){
            steps{
                withCredentials([aws(accessKeyVariable: ${AWS_ACCESS_KEY_ID}, credentialsId: ${AWS_KEYS}, secretKeyVariable: ${AWS_SECRET_ACCESS_KEY})]) {
                    sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
                    sh "docker push ${AWS_ACCESS_KEY_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/space-registry:${params.IMAGE_TAG}"    
                }
            }

        }
    }

    post{
        success{
            echo "YES!!! Docker image has been pushed. Tag is :${params.IMAGE_TAG}"
        }
        failure{
            echo "Too bad. Build is failed."

        }
    }
}
