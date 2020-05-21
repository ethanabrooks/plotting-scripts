#!/usr/bin/env zsh
plot --names Ours 'No roll' 'No scan' 'No roll or scan' 'OLSK' Transformer --paths ~/neurips/ours ~/neurips/no-roll ~/neurips/no-scan ~/neurips/no-roll-or-scan ~/neurips/olsk ~/neurips/transformer --tag success --limit 80000000 --fname ~/neurips/rewards-1-10
