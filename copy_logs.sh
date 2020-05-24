#! /usr/bin/env bash
scp -r rldl14:~/ppo/.runs/logdir/control-flow/pretrained/world-size6/control-flow/3conditions/transformer/paper/train1-10/eval10-50/ ~/neurips/transformer
scp -r rldl14:~/ppo/.runs/logdir/control-flow/pretrained/world-size6/control-flow/3conditions/no-roll-or-scan/paper/train1-10/eval10-50/ ~/neurips/no-roll-or-scan
scp -r rldl16:~/ppo/.runs/logdir/control-flow/pretrained/world-size6/control-flow/3conditions/olsk/paper/train1-10/eval10-50/ ~/neurips/olsk
scp -r rldl16:~/ppo/.runs/logdir/control-flow/pretrained/world-size6/control-flow/3conditions/no-scan/paper/train1-10/eval10-50/ ~/neurips/no-scan
scp -r rldl16:~/ppo/.runs/logdir/control-flow/pretrained/world-size6/control-flow/3conditions/no-roll/paper/train1-10/eval10-50/ ~/neurips/no-roll
scp -r rldl17:~/ppo/.runs/logdir/control-flow/pretrained/world-size6/paper/3conditions/train1-10/eval10-50/ ~/neurips/ours
