# The name of this Python package, or the parent package if this is a
# namespaced package.
PYTHON_PKG_NAME=cbra

# The subpackage name in a packaging namespace.
#PYTHON_SUBPKG_NAME = $(error Set PYTHON_SUBPKG_NAME in config.mk)

# Choose from 'application' or 'package'.
PROJECT_KIND=package

# Choose from 'parent' or 'namespaced'. If you are not sure, choose 'parent'.
# If PROJECT_SCOPE=namespaced, then PYTHON_SUBPKG_NAME must also be set.
PROJECT_SCOPE=parent

# The Python version to use.
PYTHON_VERSION = 3.10

# Tables to truncate when invoking `make dbtruncate`, separated by a space.
#RDBMS_TRUNCATE=

# Components to configure.
mk.configure += python python-package python-gitlab python-docs docker
mk.configure +=

test.coverage := 100

# User-defined
build.alpine.packages += libxml2-dev libxslt-dev
build.debian.packages += libxml2-dev libxslt-dev
ifdef DEV_GOOGLE_APPLICATION_CREDENTIALS
GOOGLE_APPLICATION_CREDENTIALS=$(DEV_GOOGLE_APPLICATION_CREDENTIALS)
endif
LOG_LEVEL=DEBUG
OS_RELEASE_ID ?= debian
OS_RELEASE_VERSION ?= 11
export PYTHONPATH=$(PYTHONPATH):./examples/orderapp

ifdef CI_COMMIT_REF_NAME
BRANCH_NAME=$(CI_COMMIT_REF_NAME)
endif
DOCS_BASE_PATH="python/cbra"
DOCS_GS_BUCKET=unimatrix-docs
MINOR_VERSION=$(shell cut -d '.' -f 1,2 <<< "$$(cat VERSION)")
APP_SIGNING_KEY ?= local:///pki/sig.key?alg=EdDSA&curve=Ed448
APP_ENCRYPTION_KEY ?= local:///pki/enc.key?kty=RSA&alg=RSA-OAEP-256
OAUTH_SERVER = https://oauth2.webidentityapis.com
OAUTH_SERVICE_CLIENT = cbra
export


google-authenticate:
ifdef GOOGLE_APPLICATION_CREDENTIALS
	@gcloud auth activate-service-account --key-file $(GOOGLE_APPLICATION_CREDENTIALS)
endif


deploy-docs-google-%:
	@gsutil -m cp -r 'public/*' gs://$(DOCS_GS_BUCKET)/$(DOCS_BASE_PATH)/$(*)
	@printf "Invalidating cache for docs.unimatrixone.io/$(DOCS_BASE_PATH)/$(*).\n"
	@gcloud compute url-maps invalidate-cdn-cache copernicus \
    --host docs.unimatrixone.io\
    --path "/$(DOCS_BASE_PATH)/$(*)/*"\
		--project unimatrixinfra


deploy-docs: public google-authenticate
	@printf "\nDeploying documentation for version $(MINOR_VERSION) "
	@printf "to base path $(DOCS_BASE_PATH)/$(MINOR_VERSION).\n"
	@gsutil -m cp -r 'public/*' gs://$(DOCS_GS_BUCKET)/$(DOCS_BASE_PATH)/$(MINOR_VERSION)
	@printf "Invalidating cache for docs.unimatrixone.io/$(DOCS_BASE_PATH)/$(MINOR_VERSION).\n"
	@gcloud compute url-maps invalidate-cdn-cache copernicus \
    --host docs.unimatrixone.io\
    --path "/$(DOCS_BASE_PATH)/$(MINOR_VERSION)/*"\
		--project unimatrixinfra
ifeq ($(BRANCH_NAME), mainline)
	@printf "\nDeploying documentation for latest "
	@printf "to base path $(DOCS_BASE_PATH)/latest.\n"
	@make deploy-docs-google-latest
endif
ifeq ($(BRANCH_NAME), stable)
	@printf "\nDeploying documentation for stable "
	@printf "to base path $(DOCS_BASE_PATH)/stable.\n"
	@make deploy-docs-google-stable
endif

update-headless:
	@cp -R ~/src/unimatrixone/libraries/python-unimatrix/headless/headless/*\
		$(CURDIR)/.lib/python/runtime/headless/
