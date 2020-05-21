#!/usr/bin/env zsh
plot --names Ours 'No roll' 'No scan' 'No roll or scan' 'OLSK' Transformer --paths ~/neurips/ours ~/neurips/no-roll ~/neurips/no-scan ~/neurips/no-roll-or-scan ~/neurips/olsk ~/neurips/transformer --tag eval_success_20 --limit 80000000 --fname ~/neurips/rewards-20-30
