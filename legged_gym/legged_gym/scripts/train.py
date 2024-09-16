# SPDX-FileCopyrightText: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2021 ETH Zurich, Nikita Rudin

from legged_gym.envs import *
from legged_gym.utils import get_args, task_registry, class_to_dict
import wandb

def train(args):
    env, env_cfg = task_registry.make_env(name=args.task, args=args, is_highlevel=(args.task == "go1_highlevel"))
    print("make env ok!")
    ppo_runner, train_cfg = task_registry.make_alg_runner(env=env, name=args.task, args=args)
    if train_cfg.use_wandb:
        if args.task == "cyber2_stand_dance":
            project_name = "isaacgym-cyber2-stand-dance"
        elif args.task == "cyber2_stand_dance_aug":
            project_name = "isaacgym-cyber2-stand-dance-aug"
        elif args.task == "cyber2_stand_dance_emlp":
            project_name = "isaacgym-cyber2-stand-dance-emlp"
        elif args.task == 'cyber2_push_door':
            project_name = "isaacgym-cyber2-push-door"
        elif args.task == 'cyber2_push_door_aug':
            project_name = "isaacgym-cyber2-push-door-aug"
        elif args.task == 'cyber2_push_door_emlp':
            project_name = "isaacgym-cyber2-push-door-emlp"
        elif args.task == 'cyber2_walk_slope':
            project_name = "isaacgym-cyber2-walk-slope"
        elif args.task == 'cyber2_walk_slope_aug':
            project_name = "isaacgym-cyber2-walk-slope-aug"
        elif args.task == 'cyber2_walk_slope_emlp':
            project_name = "isaacgym-cyber2-walk-slope-emlp"
        else:
            raise NotImplementedError
        wandb.init(
            config={"env_cfg": class_to_dict(env_cfg), "train_cfg": class_to_dict(train_cfg)}, 
            project=project_name, 
            name=train_cfg.runner.run_name
        )
    print("ready to learn!!!")
    ppo_runner.learn(num_learning_iterations=train_cfg.runner.max_iterations, init_at_random_ep_len=(args.task != "go1_highlevel"))

if __name__ == '__main__':
    args = get_args()
    train(args)
