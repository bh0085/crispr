#README for /crispr

## Directories
### ./query_server ##
python code handling CRISPR spacer queries

### ./cfront ##
version 0 website for crispr frontend, "cfront"

## Misc 
### Modifications to .bashrc

```bash
source ${HOME}/crispr/bin/init_env.sh
export CFRONTROOT=${HOME}/crispr/cfront
export CFRONTBIN=${CFRONTROOT}/cfront/bin
export CFRONTDATA=${HOME}/data/cfront
PATH=${PATH}:${CFRONTBIN}
```
