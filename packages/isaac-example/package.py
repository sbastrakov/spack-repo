# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# Authors: Axel Huebl
from spack import *


class IsaacExample(CMakePackage):
    """In Situ Animation of Accelerated Computations: Example Visualization Plugin"""

    homepage = "http://computationalradiationphysics.github.io/isaac/"
    url      = "https://github.com/ComputationalRadiationPhysics/isaac/archive/v1.3.1.tar.gz"
    maintainers = ['ax3l']

    version('develop', branch='dev',
            git='https://github.com/ComputationalRadiationPhysics/isaac.git')
    version('master', branch='master',
            git='https://github.com/ComputationalRadiationPhysics/isaac.git')
    version('1.3.1', '7fe075f9af68d05355eaba0e224f20ca')

    variant('cuda', default=False,
            description='Generate CUDA example for Nvidia GPUs')
    variant('alpaka', default=True,
            description='Generate CPU example via Alpaka (OpenMP 2)')

    depends_on('cmake@3.3:', type='build')
    depends_on('isaac+cuda', type='link', when='+cuda')
    depends_on('isaac~cuda', type='link', when='~cuda')
    depends_on('icet') # aww....
    depends_on('alpaka', type='link', when='+alpaka')

    root_cmakelists_dir = 'example'

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DISAAC_CUDA:BOOL={0}'.format((
                'ON' if '+cuda' in spec else 'OFF')),
            '-DISAAC_ALPAKA:BOOL={0}'.format((
                'ON' if '+alpaka' in spec else 'OFF')),
            '-DISAAC_DIR={0}'.format(
                spec['isaac'].prefix)
        ]
        if '+alpaka' in spec:
            args.append('-DALPAKA_ROOT={0}'.format(
                spec['alpaka'].prefix))
            if '~cuda' in spec:
                args.append('-DALPAKA_ACC_GPU_CUDA_ENABLE:BOOL=OFF')
        return args

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if '+alpaka' in spec:
            install('spack-build/example_alpaka', join_path(prefix.bin, 'example_alpaka'))
        if '+cuda' in spec:
            install('spack-build/example_cuda', join_path(prefix.bin, 'example_cuda'))
