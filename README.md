README for /crispr

# Directories
## ./query_server ##
python code handling CRISPR spacer queries

## ./frontend ##
frontend mockups and soon a completed website for the CRISPR region submission endpoint

css, html, javascript


# Misc 
## Modifications to .bashrc

<code>
source ${HOME}/crispr/bin/init_env.sh

export CFRONTROOT=${HOME}/crispr/cfront

export CFRONTBIN=${CFRONTROOT}/cfront/bin

export CFRONTDATA=${HOME}/data/cfront

PATH=${PATH}:${CFRONTBIN}
</code>
