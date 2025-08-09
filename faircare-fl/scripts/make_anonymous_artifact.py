import os
import shutil
import tempfile

IGNORE = ['.git', 'runs']

def main():
    dst = 'artifact'
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree('.', dst, ignore=shutil.ignore_patterns(*IGNORE))
    print('Artifact written to', dst)

if __name__ == '__main__':
    main()
