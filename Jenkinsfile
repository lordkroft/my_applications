properties([pipelineTriggers([githubPush()])])

pipeline{
    options {
        skipDefaultCheckout true
    }
    
    agent any
        stages{  
        stage("Checkout to target branch"){
            steps{
                dir("${env.WORKSPACE}"){
                    git url: "https://github.com/lordkroft/my_applications.git", credentialsId: 'ddfd73cb-1789-4fd9-8ac4-21f81b8f5407', branch: "master", poll: true
                }
            }
        }
    
        
        stage("Building image"){
            steps{
                    sh "pwd"
                    sh "ls -la"
                    sh "docker build  -t 413752907951.dkr.ecr.us-east-2.amazonaws.com/frontend:${params.IMAGE_TAG} -f front/Dockerfile ." 
                    sh "docker build  -t 413752907951.dkr.ecr.us-east-2.amazonaws.com/backend:${params.IMAGE_TAG} -f backend/Dockerfile ."
                }
            }
        stage("Pushing to ECR"){
            steps{
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'lordkroft', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh "/usr/local/bin/aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 413752907951.dkr.ecr.us-east-2.amazonaws.com"
                    sh "docker push 413752907951.dkr.ecr.us-east-2.amazonaws.com/frontend:${params.IMAGE_TAG}"
                    sh "docker push 413752907951.dkr.ecr.us-east-2.amazonaws.com/backend:${params.IMAGE_TAG}"
                }
            }

        }
    


        stage("Get current Task Definition"){
            steps{
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'lordkroft', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh "/usr/local/bin/aws ecs describe-services --service service --cluster my_ecs_app --region us-east-2"
                    sh "/usr/local/bin/aws ecs describe-task-definition --task-definition my_ecs_app_task:${params.REVISION} --region us-east-2"
                }
            }
        }
        stage("Register new version of task-definition"){
            when{
                expression {
                    params.UPDATE
                }
            }
            steps{
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'lordkroft', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                sh "/usr/local/bin/aws ecs register-task-definition --region us-east-2 --family my_ecs_app_task --cli-input-json file://task_defenition_app.json" 
                }
            }
        }
        stage("Update"){
            when{
                expression {
                    params.UPDATE
                }
            }
            steps{
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'lordkroft', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh "/usr/local/bin/aws ecs update-service --region us-east-2 --cluster my_ecs_app --service service --task-definition my_ecs_app_task:${params.NEW_REVISION} --force-new-deployment --health-check-grace-period-seconds 180"
                }
            }

        }
    }
}

