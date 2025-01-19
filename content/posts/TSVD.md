+++
date = 2024-01-19
draft = false
title = 'Efficient Scalable Thread-Safety-Violation Detection'
weight = 10
tags = ["paper-summary"]
+++

> Paper: [Efficient Scalable Thread-Safety-Violation Detection](https://dl.acm.org/doi/pdf/10.1145/3341301.3359638)

- Existing solutions
	- Static or dynamic analysis to identify the potential buggy locations to inject delays.
		- Injects small number of delays but large analysis time
	- Inject probabilistic random delays
		- Inject large number of delays but small analysis time
	- TSVD tries to find the middle ground
- TSVD employs two techniques to select the points to inject delays
	- Near miss tracking
	- Happens before relationship identification
- Near miss tracking
	- Identify two operations on a thread-unsafe object, one of which is write and happens close to each other on different threads
	- If the time difference falls within the threshold, mark it as dangerous pair
- Happens Before relationship identification
	- If adding a delay at location 1 delays the execution of the location 2.
- Delay is injected on all such pairs
	- Delay is decayed if a pair does not trigger error
	- Once the probability of delay drops to 0, the pair is removed from dangerous pair list
- Built to support .NET projects
	- Instrumentation and Runtime library
- Evaluation
	- Why some bugs were missed?
		- Two operations are close to each other only on some rare executions
		- False positive happens before prediction
		- Delay injection was not sufficient to capture the bugs
