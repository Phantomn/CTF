#!/bin/bash
service postfix start;
service uwsgi start;
service nginx start;
sleep infinity