from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import operator_benchmark as op_bench
import torch


"""Microbenchmarks for channel_shuffle operator."""


# Configs for PT channel_shuffle operator
channel_shuffle_long_configs = op_bench.cross_product_configs(
    batch_size=[1, 2, 4],
    channels_per_group=[16, 32, 64],
    height=[16, 32, 64],
    width=[16, 32, 64],
    groups=[1, 2, 4],
    tags=["long"]
)


channel_shuffle_short_configs = op_bench.config_list(
    attr_names=["batch_size", "channels_per_group", "height", "width", "groups"],
    attrs=[
        [1, 16, 16, 16, 1],
        [2, 16, 16, 16, 2],
        [2, 32, 32, 32, 2],
        [4, 32, 32, 32, 4],
        [4, 64, 64, 64, 4],
    ],
    tags=["short"]
)


class ChannelSHuffleBenchmark(op_bench.TorchBenchmarkBase):
    def init(self, batch_size, channels_per_group, height, width, groups):
        channels = channels_per_group * groups
        data_shape = (batch_size, channels, height, width)
        self.input_data = torch.rand(data_shape)
        self.groups = groups
        self.set_module_name('channel_shuffle')

    def forward(self):
        return torch.channel_shuffle(self.input_data, self.groups)


op_bench.generate_pt_test(channel_shuffle_short_configs + channel_shuffle_long_configs,
                          ChannelSHuffleBenchmark)


if __name__ == "__main__":
    op_bench.benchmark_runner.main()
