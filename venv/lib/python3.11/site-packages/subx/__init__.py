# -*- coding: utf-8 -*-

import logging
import os

import subprocess
from subprocess import CalledProcessError


logger = logging.getLogger(__name__)


def call(cmd, data=None, assert_zero_exit_status=True, warn_on_non_zero_exist_status=False, **kwargs):
    """
    :rtype: SubprocessResult

    Raises OSError if command was not found

    Returns non-zero result in result.ret if subprocess terminated with non-zero exist status.
    """
    if (not kwargs.get('shell')) and isinstance(cmd, (str, bytes)):
        raise ValueError('cmd should be list or tuple, not a string: %r' % cmd)
    result = SubprocessResult.call(cmd, data=data, **kwargs)
    if assert_zero_exit_status and result.ret != 0:
        raise SubprocessError(result)

    if warn_on_non_zero_exist_status and result.ret != 0:
        logger.warning('subprocess failed %r' % result)

    return result


class SubprocessResult(object):
    def __init__(self, cmd, ret, stdout=b'', stderr=b''):
        self.cmd = cmd
        self.ret = ret
        if isinstance(stdout, str):
            stdout = stdout.encode('ascii')
        if isinstance(stderr, str):
            stderr = stderr.encode('ascii')

        self.stdout = stdout
        self.stderr = stderr

    max_head_size = 4000

    def __repr__(self):
        byte_prefix = ''
        cmd = self.cmd_for_copy_and_paste.encode('ascii', 'backslashreplace').decode('ascii')
        stdout_rep = repr(self.head_of_string(self.stdout))
        stderr_rep = repr(self.head_of_string(self.stderr))
        return '<{} cmd={} ret={} stdout={}{} stderr={}{}>'.format(self.__class__.__name__,
                                                                   cmd,
                                                                   self.ret,
                                                                   byte_prefix, stdout_rep,
                                                                   byte_prefix, stderr_rep)

    @property
    def cmd_for_copy_and_paste(self):
        ret = []
        for item in self.cmd:
            if ' ' in item:
                item = '{}'.format(item)
            ret.append(item)
        ret = ' '.join(ret)
        return "'{}'".format(ret)

    @classmethod
    def head_of_string(cls, stdout, max_head_size=None):
        if stdout is None:
            return b'None'
        assert isinstance(stdout, bytes)
        if not max_head_size:
            max_head_size = cls.max_head_size
        stdout = stdout.strip()
        if len(stdout) < max_head_size:
            return stdout
        return b'%s ... [cut]' % stdout[:max_head_size]

    @classmethod
    def _cleanup(cls, stdin):
        try:
            stdin.close()
        except AttributeError:
            pass

    @classmethod
    def call(cls, cmd, data=None, **kwargs):
        kwargs['start_new_session'] = kwargs.get('start_new_session',
                                                 True)  # change default. We want sudo to fail, not to read a password from /dev/tty
        kwargs.setdefault('bufsize', -1)
        timeout = kwargs.pop('timeout', None)
        if data:
            stdin = subprocess.PIPE
        else:
            stdin = open(os.devnull, 'rb')
        if 'stderr' not in kwargs:
            kwargs['stderr'] = subprocess.PIPE
        try:
            pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=stdin, **kwargs)
        except OSError:
            cls._cleanup(stdin=stdin)
            raise

        stdout, stderr = handle_subprocess_pipe_with_timeout(pipe, timeout=timeout, data=data)
        cls._cleanup(stdin=stdin)
        return cls(cmd, pipe.wait(), stdout, stderr)


class SubprocessError(CalledProcessError):
    def __init__(self, subprocess_result):
        super(SubprocessError, self).__init__(subprocess_result.ret, subprocess_result.cmd,
                                              SubprocessResult.head_of_string(subprocess_result.stdout))
        self.stderr = SubprocessResult.head_of_string(subprocess_result.stderr)

    def __str__(self):
        return '{}: stdout={} stderr={}'.format(super(SubprocessError, self).__str__(),
                                                    repr(self.output), repr(self.stderr))


def handle_subprocess_pipe_with_timeout(pipe, timeout, data=None):
    if (data is not None) and not pipe.stdin:
        raise Exception('pipe.stdin must be a stream if you pass in data')
    stdout = ''
    stderr = ''
    kwargs = dict(input=data)
    if timeout:
        kwargs['timeout'] = timeout
    try:
        stdout, stderr = pipe.communicate(**kwargs)
    except subprocess.TimeoutExpired:
        pipe.kill()
        try:
            # Other solution to handle timeout for shell=True: http://stackoverflow.com/a/4791612/633961
            # related: http://stackoverflow.com/questions/36592068/subprocess-with-timeout-what-to-do-after-timeoutexpired-exception
            stdout, stderr = pipe.communicate(timeout=0.1)
        except subprocess.TimeoutExpired:
            pass
        raise subprocess.TimeoutExpired(pipe.args, timeout, 'stdout: %r stderr: %r' % (stdout, stderr))
    return stdout, stderr
