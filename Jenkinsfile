properties([pipelineTriggers([githubPush()])])

pipeline{
    options {
        skipDefaultCheckout true
    }

    agent any
    parameters{
        string(defaultValue: 'service', name: 'ECS_SERVICE')
        string(defaultValue: 'my_ecs_app', name: 'ECS_CLUSTER')
        string(defaultValue: 'us-east-2', name: 'REGION')
        string(defaultValue: 'my_ecs_app-task', name: 'FAMILY', description: 'task_definition')
	string(defaultValue: 'latest', name: 'NEW_REVISION', description: 'New ver of task_definition file')
	string(defaultValue: 'latest', name: 'REVISION', description: 'Previous ver of task_definition file')
        string(defaultValue: 'task_defenition_app.json', name: 'PATH', description: 'task_definition file')
        string(defaultValue: 'master', name: 'BRANCH', description: 'task_definition file')
	string(defaultValue: 'true', name: 'UPDATE')
        string(defaultValue: 'latest', name: 'IMAGE_TAG')
    }
    stages{  
        stage("Checkout to target branch"){
            steps{
                dir("master-${BUILD_NUMBER}"){
                    git url: "https://github.com/lordkroft/my_applications.git", credentialsId: 'ba5670d4-158b-41f3-908e-039781f6ecd7', branch: "master", poll: true
                }
            }
        }
    
        
        stage("Building image"){
            steps{
                    sh "docker build -t 413752907951.dkr.ecr.${params.REGION}.amazonaws.com/frontend:${params.IMAGE_TAG} ." 
                    sh "docker build -t 413752907951.dkr.ecr.${params.REGION}.amazonaws.com/backend:${params.IMAGE_TAG} ."
                }
            }
        stage("Pushing to ECR"){
            steps{
                withCredentials([aws(accessKeyVariable: ${AWS_ACCESS_KEY_ID}, credentialsId: 'lordkroft', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh "aws ecr get-login-password --region ${params.REGION} | docker login --username AWS --password-stdin 413752907951.dkr.ecr.${params.REGION}.amazonaws.com"
                    sh "docker push ${AWS_ACCESS_KEY_ID}.dkr.ecr.${params.REGION}.amazonaws.com/space-registry:${params.IMAGE_TAG}"    
                }
            }

        }
    

//    post{
//        success{
//            echo "YES!!! Docker image has been pushed. Tag is :${params.IMAGE_TAG}"
//        }
//        failure{
//            echo "Too bad. Build is failed."
//
//        }
//    }
        

     
        stage("Get current Task Definition"){
            steps{
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'lordkroft', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh "aws ecs describe-services --service ${params.ECS_SERVICE} --cluster ${params.ECS_CLUSTER} --region ${params.REGION}"
                    sh "aws ecs describe-task-definition --task-definition ${params.FAMILY}:${params.REVISION} --region ${params.REGION}"
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
                    sh "aws ecs register-task-definition --region ${params.REGION} --family ${params.FAMILY} --cli-input-json file://${params.PATH}"
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
                    sh "aws ecs update-service --region ${params.REGION} --cluster ${params.ECS_CLUSTER} --service ${params.ECS_SERVICE} --task-definition ${params.TASK_DEFINITION}:${params.NEW_REVISION} --force-new-deployment --health-check-grace-period-seconds 180"
                }
            }

        }
    }
}
