from __future__ import print_function
import math

from hurry.filesize import size

__author__ = 'dominiczippilli'


def billing_bucket(t):
    """
    Returns billing bucket for AWS Lambda.
    :param t: An elapsed time in ms.
    :return: Nearest 100ms, rounding up, as int.
    """
    return int(math.ceil(t / 100.0)) * 100


def render_result(verbose, lambdapath, result, exec_clock, exec_rss):
    """
    Render the result of a lambda execution, with profiling info if verbose.
    :param lambdapath: Path given for the lambda.
    :param result: Result of the execution.
    :param exec_clock: Execution clock time.
    :param exec_rss: Execution RSS.
    :return: Void.
    """
    if verbose:
        print('Executed %s' % lambdapath)
        print('Estimated...')
        print('...execution clock time:\t\t %ims (%ims billing bucket)' % (exec_clock, billing_bucket(exec_clock)))
        print('...execution peak RSS memory:\t\t %s (%i bytes)' % (size(exec_rss), exec_rss))
        print('----------------------RESULT----------------------')
    print(str(result))


def render_summary(stats):
    """
    Render summary of an event stream run.
    :param stats: Dictionary('clock':list()<float>, 'rss':list()<int>)
    :return: Void.
    """
    print('\nSummary profile from stream execution:')
    print('Samples: %i' % len(stats['clock']))
    if -1 in stats['clock']:
        print('(ERRORS DETECTED: Removing timing samples from aborted invocations.)')
        stats['clock'] = [x for x in stats['clock'] if x > 0]
        print('New sample size: %i' % len(stats['clock']))
    median = sorted(stats['clock'])[math.trunc(len(stats['clock']) / 2)]
    print(stats['clock'])
    mean =  math.fsum(stats['clock'])/len(stats['clock'])
    print('Clock time:\n'
          '\tMin: %ims, Max: %ims, Median: %ims, Median Billing Bucket: %ims, Rounded Standard Deviation: %sms' % (
              min(stats['clock']),
              max(stats['clock']),
              median,
              billing_bucket(median),
              math.trunc(math.ceil(math.sqrt(math.fsum((x-mean)**2 for x in stats['clock'])/(len(stats['clock'])-1))))
          )) if len(stats['clock']) > 0 else print("No valid timing samples!")
    print('Peak resident set size (memory):\n'
          '\tMin: %s, Max: %s' % (
              size(min(stats['rss'])),
              size(max(stats['rss']))
          ))