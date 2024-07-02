#!groovy
@Library(['cop-pipeline-bootstrap']) _
loadPipelines()

def appName = 'productfinder-crawler'
// def version,

def config = [
    agentLabel: 'china',
    usePraDispatch: false,
    tags: [
        'Name'              : appName,
        'costcenter'        : '104420',
        'classification'    : 'Bronze',
        'email'             : 'frank.zhao@nike.com',
        'nike-owner'        : 'product-finder',
        'nike-department'   : 'Web Eng - nike.com Cloud Capability',
        'nike-domain'       : 'launch',
        'nike-application'  : appName,
        'nike-distributionlist': 'Lst-digitaltech.GC.LaunchServices@Nike.com',
        'nike-environment': 'test'

    ],
    buildFlow: [
        DEVELOP : ['AMI'],
    ],
    branchMatcher: [
        RELEASE: ['main'],
        DEVELOPMENT: ['^(?!main$).*$']
    ],
    build: [
        cmd: './build.sh'
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
        [from: 'requirements.txt', into: '/opt/pyth/crawler'],
        [from: 'build.sh', into: '/opt/pyth/crawler'],
        [from: 'cron_run.sh', into: '/opt/pyth/crawler'],
        [from: 'sync_launch_product.py', into: '/opt/pyth/crawler'],
        [from: 'send_slack_notification.py', into: '/opt/pyth/crawler']
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
    deploymentEnvironment: [
        chinatest: [
            agentLabel: 'china',
            cloudEnvironment: 'test',                  
            deploy: [
                // Account Information
                accountId                     : '734176943427',
                region                        : 'cn-northwest-1',
                awsAssumeRole                 : 'arn:aws-cn:iam::734176943427:role/launch-productfinder-bmx-deploy-role',
                vpcId                         : 'vpc-069713cbc0909398d',
                subnets                       : ['subnet-07d67d2fece2fc924'],
                securityGroups                : ['sg-02a528cbf272abe21'],
                desiredCapacity               : '1',
                maxSize                       : '1',
                minSize                       : '1',
                instanceType                  : 't3.micro',
                iamInstanceProfile            : 'arn:aws-cn:iam::734176943427:instance-profile/launch.product-catalog-insights-frontend',
                associatePublicIp             : false,
                ebsOptimized                  : false,
                includeDefaultScheduledActions: false,
            ],
            deployFlow: [
                DEVELOP: ["Deploy"],
            ],
            tags: [
                'nike-owner': 'frank.zhao@nike.com',
                'nike-distributionlist': 'Lst-digitaltech.GC.LaunchServices@Nike.com',
                'nike-environment': 'test'
            ]
        ]
    ]

]

ec2BlueGreenDeployPipeline(config)