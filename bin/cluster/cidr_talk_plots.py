from fabric.api import *
from pymongo import MongoClient
import pymongo
from mongo_utils import *
import datetime
import json
from time import sleep, time, strftime, gmtime, localtime
import os.path
import pprint
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from hosts import velox_hosts

from velox_fabric import MONGO_HOST, MONGO_DB, MONGO_PORT, BenchmarkConfig


MONGO_HOST = "ec2-54-161-215-250.compute-1.amazonaws.com"
MONGO_PORT = 27017

MONGO_DB = "cs286_final_project"

size1 = (4.5, 3.1)
size2 = (5, 3.1)


figdir = "cidr_talk_plots"



def convert_hostname(h):
    return unicode(h.replace(".", "_"))

# @task
# def plot_all_micros():
#     caching_mf_thru()
#     caching_mf_lat()
#     caching_news_thru()
#     caching_news_lat()
#     updates_news_thru()
#     updates_news_pred_lat()
#     updates_news_obs_lat()

    



@task
def caching_news_lat():
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    coll = db["micro_caching_news"]

#######################################################################
    ft_false_pr_false_ys = {"dl": [], "p95": [], "mean": []}
    ft_false_pr_false_filter = {
            "config.cache_features": False,
            "config.cache_predictions": False,
            }

    ft_false_pr_false_results = coll.find(ft_false_pr_false_filter).sort([("config.doc_length", pymongo.ASCENDING)])

    skipfirst = True
    for result in ft_false_pr_false_results:
        if skipfirst:
            skipfirst = False
            continue

        ft_false_pr_false_ys["dl"].append(result[u'config'][u'doc_length'])
        servers = result[u'servers']
        p95 = 0.0
        mean = 0.0
        for s, val in servers.iteritems():
            pred = val[u'metrics_json'][u'timers'][u"newsgroups/predict/"]
            p95 += pred[u'p95']
            mean += pred[u'mean']
        p95 = p95 / 3.0 * 1000.0
        mean = mean / 3.0 * 1000.0
        ft_false_pr_false_ys["p95"].append(p95)
        ft_false_pr_false_ys["mean"].append(mean)


#######################################################################

    ft_false_pr_true_ys = {"dl": [], "p95": [], "mean": []}
    ft_false_pr_true_filter = {
            "config.cache_features": False,
            "config.cache_predictions": True,
            }

    ft_false_pr_true_results = coll.find(ft_false_pr_true_filter).sort([("config.doc_length", pymongo.ASCENDING)])

    for result in ft_false_pr_true_results:
        # doc_lengths.append(result[u'config'][u'doc_length'])
        ft_false_pr_true_ys["dl"].append(result[u'config'][u'doc_length'])
        servers = result[u'servers']
        p95 = 0.0
        mean = 0.0
        for s, val in servers.iteritems():
            pred = val[u'metrics_json'][u'timers'][u"newsgroups/predict/"]
            p95 += pred[u'p95']
            mean += pred[u'mean']
        p95 = p95 / 3.0 * 1000.0
        mean = mean / 3.0 * 1000.0
        ft_false_pr_true_ys["p95"].append(p95)
        ft_false_pr_true_ys["mean"].append(mean)

#######################################################################
    ft_true_pr_false_ys = {"dl": [], "p95": [], "mean": []}
    ft_true_pr_false_filter = {
            "config.cache_features": True,
            "config.cache_predictions": False,
            }

    ft_true_pr_false_results = coll.find(ft_true_pr_false_filter).sort([("config.doc_length", pymongo.ASCENDING)])

    for result in ft_true_pr_false_results:
        # doc_lengths.append(result[u'config'][u'doc_length'])
        ft_true_pr_false_ys["dl"].append(result[u'config'][u'doc_length'])
        servers = result[u'servers']
        p95 = 0.0
        mean = 0.0
        for s, val in servers.iteritems():
            pred = val[u'metrics_json'][u'timers'][u"newsgroups/predict/"]
            p95 += pred[u'p95']
            mean += pred[u'mean']
        p95 = p95 / 3.0 * 1000.0
        mean = mean / 3.0 * 1000.0
        ft_true_pr_false_ys["p95"].append(p95)
        ft_true_pr_false_ys["mean"].append(mean)

#######################################################################
    ft_true_pr_true_ys = {"dl": [], "p95": [], "mean": []}
    ft_true_pr_true_filter = {
            "config.cache_features": True,
            "config.cache_predictions": True,
            }

    ft_true_pr_true_results = coll.find(ft_true_pr_true_filter).sort([("config.doc_length", pymongo.ASCENDING)])

    for result in ft_true_pr_true_results:
        # doc_lengths.append(result[u'config'][u'doc_length'])
        ft_true_pr_true_ys["dl"].append(result[u'config'][u'doc_length'])
        servers = result[u'servers']
        p95 = 0.0
        mean = 0.0
        for s, val in servers.iteritems():
            pred = val[u'metrics_json'][u'timers'][u"newsgroups/predict/"]
            p95 += pred[u'p95']
            mean += pred[u'mean']
        p95 = p95 / 3.0 * 1000.0
        mean = mean / 3.0 * 1000.0
        ft_true_pr_true_ys["p95"].append(p95)
        ft_true_pr_true_ys["mean"].append(mean)




    format_strs = ['^--', '^-']
    colors=['#348ABD', '#7A68A6', '#A60628', '#467821', '#CF4457', '#188487', '#E24A33']
    fig, ax = plt.subplots()

    # ax.plot(ft_false_pr_false_ys["dl"], ft_false_pr_false_ys["mean"], format_strs[0], color=colors[0], label="No Caching mean")
    ax.plot(ft_false_pr_false_ys["dl"], ft_false_pr_false_ys["p95"], format_strs[1], color=colors[0], label="No Caching")

    # ax.plot(ft_false_pr_true_ys["dl"], ft_false_pr_true_ys["mean"], format_strs[0], color=colors[1], label="Cache Prediction mean")
    # ax.plot(ft_false_pr_true_ys["dl"], ft_false_pr_true_ys["p95"], format_strs[1], color=colors[1], label="Cache Pred.")

    # ax.plot(ft_true_pr_false_ys["dl"], ft_true_pr_false_ys["mean"], format_strs[0], color=colors[2], label="Cache Features mean")
    ax.plot(ft_true_pr_false_ys["dl"], ft_true_pr_false_ys["p95"], format_strs[1], color=colors[2], label="Cache Features")

    # ax.plot(ft_true_pr_true_ys["dl"], ft_true_pr_true_ys["mean"], format_strs[0], color=colors[3], label="Cache Features and Predictions mean")
    # ax.plot(ft_true_pr_true_ys["dl"], ft_true_pr_true_ys["p95"], format_strs[1], color=colors[3], label="Cache Both")


    # ax.set_title("Affect of Caching on Pred. Lat.")
    ax.set_xlabel("Feature Complexity")
    ax.set_ylabel("95% Prediction latency (ms)")
    # ax.legend(loc=0, prop={'size': 10})
    ax.set_yscale('log')

    (ymin, ymax) = ax.get_ylim()
    ax.set_ylim(0.01, ymax)

    # (xmin, xmax) = ax.get_xlim()
    # ax.set_xlim(0, xmax)
    # size = (3, 2.3)
    font_size=10
    fig.set_size_inches(size1)
    for item in ([ax.xaxis.label, ax.yaxis.label] +
               ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(font_size)
    plt.tight_layout()

    local("mkdir -p %s" % figdir)
    plt.savefig("%s/%s.pdf" % (figdir, "micro_caching_news_lat"))






@task
def spark_vs_velox():
    spark_xs = [25, 50, 75, 100, 200]
    spark_thru = [1.6558499882569346, 0.7172949031443818, 0.335872815287743, 0.22414019041692462, 0.05954587803114408]
    spark_lat_mean = [303.4273210312152, 440.9160242905702, 616.1326433429523, 756.2315789355191, 1415.6032385631174]
    spark_lat_stdev = [174.5281882134465, 173.23046533759808, 182.63805404925472, 27.688544236223663, 181.06341647022302]


    query = {
            "config.num_users": 100000,
            "config.num_items": 50000,
            "config.cache_partial_sum": True,
            "config.model_type": "MatrixFactorizationModel"
            }
    model_dims = []
    pred_mean = []
    pred_stdev = []
    thruput = []

    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client["velox"]
    coll = db["crankshaw_cache_partial_sums"]

    results = coll.find(query).sort([("config.model_dim", pymongo.ASCENDING)])

    for result in results:
        model_dims.append(result[u'config'][u'model_dim'])
        servers = result[u'servers']
        mean = 0.0
        var = 0.0
        for s, val in servers.iteritems():
            pred = val[u'metrics_json'][u'timers'][u"matrixfact/predict/"]
            mean += pred[u'mean']
            var += pred[u'stddev']**2
        mean = mean / 3.0 * 1000.0
        stddev = (var / 3.0)**0.5  * 1000.0
        pred_mean.append(mean)
        pred_stdev.append(stddev)

        clients = result[u'clients']
        total_thru = 0.0
        for s, val in clients.iteritems():
            total_thru += val[u'total_thru']
        thruput.append(total_thru)

    format_strs = ['o-', 'o--']
    colors=['#348ABD', '#7A68A6', '#A60628', '#467821', '#CF4457', '#188487', '#E24A33']



    # first do latency
    fig, ax = plt.subplots()
    ax.errorbar(spark_xs, spark_lat_mean, yerr=spark_lat_stdev, fmt=format_strs[0], color=colors[0], label="Spark")
    ax.errorbar(model_dims, pred_mean, yerr=pred_stdev, fmt=format_strs[0], color=colors[2], label="Velox")

    # ax.plot(ft_false_sums_false_ys["dl"], ft_false_sums_false_ys["total_thru"], , color=colors[0], label="No Caching (Total)")
    # ax.plot(ft_false_sums_false_ys["dl"], ft_false_sums_false_ys["pred_thru"], format_strs[1], color=colors[0], label="No Caching (Prediction)")

    # ax.set_title("Pred Lat. (10% observations)")
    ax.set_xlabel("Model dimensions")
    ax.set_ylabel("Prediction latency (ms)")
    # ax.legend(loc=0, prop={'size': 10})
    ax.set_yscale('log')

    (ymin, ymax) = ax.get_ylim()
    if ymin > 0:
        ymin = 0
    ax.set_ylim(0, ymax + 200)

    (xmin, xmax) = ax.get_xlim()
    ax.set_xlim(0, xmax + 10)

    size = (4, 2.5)
    font_size=10
    fig.set_size_inches(size)
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
               ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(font_size)
    plt.tight_layout()
    local("mkdir -p %s" % figdir)
    plt.savefig("%s/%s.pdf" % (figdir, "spark_velox_pred"))



