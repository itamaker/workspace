PROJECTS = skillforge runlens ragcheck promptdeck datasetlint go-chrome-ai
REPOS = $(PROJECTS) homebrew-tap itamaker

homebrew-tap_REPO = https://github.com/itamaker/homebrew-tap.git
itamaker_REPO = https://github.com/itamaker/itamaker.git
go-chrome-ai_REPO = https://github.com/itamaker/go-chrome-ai.git
skillforge_REPO = https://github.com/itamaker/skillforge.git
runlens_REPO = https://github.com/itamaker/runlens.git
ragcheck_REPO = https://github.com/itamaker/ragcheck.git
promptdeck_REPO = https://github.com/itamaker/promptdeck.git
datasetlint_REPO = https://github.com/itamaker/datasetlint.git

.PHONY: build test sync clean

ifneq ($(filter sync,$(MAKECMDGOALS)),)
SYNC_GOAL_REPOS := $(filter $(REPOS),$(MAKECMDGOALS))
INVALID_SYNC_GOALS := $(filter-out sync $(REPOS),$(MAKECMDGOALS))
ifneq ($(strip $(INVALID_SYNC_GOALS)),)
$(error Unknown repo target(s) for sync: $(INVALID_SYNC_GOALS))
endif
.PHONY: $(REPOS)
$(REPOS):
	@:
endif

ifneq ($(strip $(SYNC_GOAL_REPOS)),)
SYNC_TARGET_REPOS := $(SYNC_GOAL_REPOS)
else
SYNC_TARGET_REPOS := $(REPOS)
endif

build:
	@for dir in $(PROJECTS); do \
		(cd $$dir && go build ./...); \
	done

test:
	@for dir in $(PROJECTS); do \
		(cd $$dir && go test ./...); \
	done

sync: $(addprefix sync-,$(SYNC_TARGET_REPOS))

clean:
	@for dir in $(REPOS); do \
		if [ -e "$$dir" ]; then \
			echo "Removing $$dir"; \
			rm -rf "$$dir"; \
		else \
			echo "Skipping $$dir: not found."; \
		fi; \
	done

sync-%:
	@if [ -d "$*/.git" ]; then \
		echo "Pulling $*"; \
		git -C "$*" pull --ff-only; \
	elif [ -e "$*" ]; then \
		echo "Skipping $*: $* exists but is not a git repository."; \
	else \
		echo "Cloning $*"; \
		git clone "$($*_REPO)" "$*"; \
	fi
