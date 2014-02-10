from fabric.api import local

def prepare_deployment():
    local('pwd')
    local('lessc static/css/styles.less > static/css/styles.css')