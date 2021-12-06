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
	string(defaultValue: '', name: 'NEW_REVISION', description: 'New ver of task_definition file')
	string(defaultValue: '', name: 'REVISION', description: 'Previous ver of task_definition file')
        string(defaultValue: 'task_defenition_app.json', name: 'PATH', description: 'task_definition file')
        string(defaultValue: 'master', name: 'BRANCH', description: 'task_definition file')
        booleanParam(name:'UPDATE', defaultValue: false, description: 'Update ECS service?')
    }

    stages{  
        stage("Checkout to target branch"){
            steps{
                dir("${params.BRANCH}-${BUILD_NUMBER}"){
                    git url: "https://github.com/lordkroft/my_applications.git", credentialsId: "lordkroft", branch: "${params.BRANCH}", poll: true
                }
            }
        }
    
            
        stage("Get current Task Definition"){
            steps{
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'AWS_KEYS', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
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
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'AWS_KEYS', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
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
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'AWS_KEYS', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh "aws ecs update-service --region ${params.REGION} --cluster ${params.ECS_CLUSTER} --service ${params.ECS_SERVICE} --task-definition ${params.TASK_DEFINITION}:${params.NEW_REVISION} --force-new-deployment --health-check-grace-period-seconds 180"
                }
            }

        }
    }
}
