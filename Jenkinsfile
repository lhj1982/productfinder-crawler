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
    branchMatcher: [
        RELEASE: ['main'],
        DEVELOPMENT: ['^(?!main$).*$']
    ],
    build: [
        cmd: 'python install -r requirements.txt'
    ],
    application: [
        name      : appName,
        group     : 'test',
        version   : '1.0',
        teamPrefix: 'test',
    ],
    package: [
       description: 'transform productfinder-crawler',
       version: '1.0',
       packageName: appName,
       priority: 'required',
       transformations: [
        [from: 'app', into: '/opt/pyth/crawler/app'],
        [from: 'app.py', into:'/opt/pyth/crawler'],
        [from: 'config.py', into: '/opt/pyth/crawler'],
        [from: 'db.py', into: '/opt/pyth/crawler'],
        [from: 'rating_calc.py', into: '/opt/pyth/crawler'],
        [from: 'weibo.py', into: '/opt/pyth/crawler'],
        [from: 'update_reviews.py', into: '/opt/pyth/crawler'],
        [from: 'update_prices.py', into: '/opt/pyth/crawler'],
        [from: 'requirements.txt', into: '/opt/pyth/crawler']
       ],
       user: 'pyth',
    ],
    smartBake: [
        chinaBakery: [
            agentLabel: 'china',
            accountId: '734176943427',
            awsRole: 'arn:aws-cn:iam::734176943427:role/launch-productfinder-bmx-deploy-role',
            region: 'cn-northwest-1',
            vpcId: 'vpc-069713cbc0909398d',
            subnets: ['subnet-02a00bec41615cf0b'],
            securityGroupName: 'CITBakingSg',
            amiSelection: ['osversion':'2004', 'quarter': '3.0', 'weeksback': ''],
        ]
    ],
    imageName: 'launch/product-catalog-insights-frontend',
    dockerFileName: 'Dockerfile',
    dockerBuildPath: '.',
    imageTags: [ "${imageVersion}", "latest" ],

    credentialsId: 'df371154-cc81-45f5-a125-fea1b341f3a1',

    qma: [qualityConfig: 'quality-config.yaml']
])