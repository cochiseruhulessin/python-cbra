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
GOOGLE_LB_NAME = docs-cochise-io
GOOGLE_LB_PROJECT = cochise-mye9xe
LOG_LEVEL=DEBUG
OS_RELEASE_ID ?= debian
OS_RELEASE_VERSION ?= 11
export PYTHONPATH=$(PYTHONPATH):./examples/orderapp

APP_SIGNING_KEY ?= local:///pki/sig.key?alg=EdDSA&curve=Ed448
APP_ENCRYPTION_KEY ?= local:///pki/enc.key?kty=RSA&alg=RSA-OAEP-256
ifdef CI_COMMIT_REF_NAME
BRANCH_NAME=$(CI_COMMIT_REF_NAME)
endif
DOCS_BASE_PATH=python/cbra
DOCS_DOMAIN=docs.cochise.io
DOCS_GS_BUCKET=docs.cochise.io
GOOGLE_DATASTORE_NAMESPACE=cbra.dev.cochise.io
GOOGLE_SERVICE_PROJECT=unimatrixdev
MINOR_VERSION=$(shell cut -d '.' -f 1,2 <<< "$$(cat VERSION)")
OAUTH_SERVER = https://oauth2.webidentityapis.com
OAUTH_SERVICE_CLIENT = cbra
export


google-authenticate:


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
	@gsutil cp -r 'public/*' gs://$(DOCS_GS_BUCKET)/$(DOCS_BASE_PATH)/$(MINOR_VERSION)/
#ifeq ($(BRANCH_NAME), mainline)
	@printf "\nDeploying documentation for latest "
	@printf "to base path $(DOCS_BASE_PATH)/latest.\n"
	@make deploy-docs-google-latest
#endif
	@printf "Invalidating cache for docs.unimatrixone.io/$(DOCS_BASE_PATH)/.\n"
	@gcloud compute url-maps invalidate-cdn-cache $(GOOGLE_LB_NAME) \
    --host $(DOCS_DOMAIN)\
    --path "/$(DOCS_BASE_PATH)/*"\
		--project $(GOOGLE_LB_PROJECT)
#ifeq ($(BRANCH_NAME), stable)
#	@printf "\nDeploying documentation for stable "
#	@printf "to base path $(DOCS_BASE_PATH)/stable.\n"
#	@make deploy-docs-google-stable
#endif

update-headless:
	@cp -R ~/src/unimatrixone/libraries/python-unimatrix/headless/headless/*\
		$(CURDIR)/.lib/python/runtime/headless/
