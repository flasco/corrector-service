# flask-corrector

## clone model
```bash
## should install git & git-lfs at first
git lfs install

git clone https://huggingface.co/shibing624/macbert4csc-base-chinese model

git clone --depth=1 https://github.com/chason777777/mgck.git sensitive-repo
# https://github.com/flasco/sensitives.git

```

## docker images

```bash
docker run --rm -d -p 3000:3000 flasco/flask-corrector # background run

docker run -it --rm -p 3000:3000 flasco/flask-corrector # with front
```
