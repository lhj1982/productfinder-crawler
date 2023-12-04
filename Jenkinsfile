#!groovy
@Library(['cicd-pipeline']) _

// Build a docker image of roster on push to master
// https://bitbucket.nike.com/projects/COP-PIPELINE/repos/cicd-pipeline/browse/vars/dockerPushPipeline.md
// https://idn.jenkins.bmx.nikecloud.com/job/Docker/job/idnroster-docker/

// String appName = ''
// String version = ''
// String teamName = 'launch'
String imageVersion = '1.0.0'

// node {
//     checkout scm
//     appName = readJSON(file: 'package.json').name
//     version = readJSON(file: 'package.json').version
// }

dockerPushPipeline([
    agentLabel: 'ec2-ondemand-agent-cn',
    usePraDispatch: false,
    buildFlow: [
        PULL_REQUEST: [],
        'Publish': ['Build Docker Image'],
    ],
    branchMatcher: ['Publish': ['main']],
    notify: [
        slack: [
            onCondition: ['Build Start', 'Success', 'Unstable', 'Failure', 'Aborted'],
            channel: '#webb-portal-deploy'
        ]
    ],
    imageName: 'launch/product-catalog-insights-frontend',
    dockerFileName: 'Dockerfile',
    dockerBuildPath: '.',
    imageTags: [ "${imageVersion}", "latest" ],

    credentialsId: 'df371154-cc81-45f5-a125-fea1b341f3a1',

    qma: [qualityConfig: 'quality-config.yaml']
])