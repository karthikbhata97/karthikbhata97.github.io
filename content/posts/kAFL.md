+++
date = 2024-01-19
draft = false
title = 'kAFL: Hardware-Assisted Feedback Fuzzing for OS Kernels'
weight = 10
tags = ["paper-summary", "fuzzing"]
+++

> Paper: [kAFL](https://nyx-fuzz.com/papers/kafl.pdf)

- Feedback fuzzing of closed source kernel mode components
- Feedback using hardware capabilities
	- Intel PT
		- Q: What does it give?
- Challenges with kernel fuzzing
	- Lots of states
	- Interrupts and threads
	- No straightforward way to "invoke" the kernel
- Technical details
	- x86-64: Kernel and userspace is split into halves
		- Total virtual address space: 2^48
			- Why?
		- Each get 2^47
		- Switching from user to kernel on syscalls do not switch page table
- Intel Processor Trace
	- Three types
		- Taken-Not-Taken: For conditional jumps, tell if a branch is taken or not
		- Target-IP: Indirect jumps, target IP
		- Flow Update Packets: Interrupts and async events.
	- Filters can be added to these
		- IP range
		- Privilege level / ring
		- CR3 filter: Only when the cr3 value matches. Helps in filtering per process
- System Design
	- Components
		- Host user space process: kAFL
		- QEMU-PT + KVM-PT for getting the processor trace from guest
		- Usermode agent in the target OS
	- Setup:
		- Agent performs a hypercall to provide kernel panic handler
		- Host patches this to get the feedback on crash
			- Instead of waiting for hte timeout
		  - Then CR3 is exchanged from agent to host
			  - This is used to set the filter
		  - Then a shared memory address is exchanged where the agent expects the input for fuzzing
		  - Fuzzing loop starts
		  - While fuzzing is being performed, the QEMU-PT decodes the trace 
		  - When the agent is done, it sends a hypercall (hc_finished).
			  - On this VM-Exit, it stops tracing
	- Fuzzing logic
		- This is the core and does similar to AFL
		- Also runs fuzzing in parallel
			- Most fuzzing is not CPU bound, so this helps
	- User mode agent
		- Broken into loader and agent
		- Agent lets you run arbitrary program, thus making it easier
		- Also loader checks if the program crashed and so it can restart
	- KVM-PT
		- This helps in tracing virtual cpu instead of logical
		- By enabling on vm-entry and disabling on vm-exit
	- QEMU-PT
		- QEMU-PT also filters the stream of executed addresses—based on previous knowledge of non-deterministic basic blocks—to prevent false-positive fuzzing results, and makes those available to the fuzzing logic as AFL-compatible bitmaps
		- ???
	- Also cache the disassembly results to speed up populating the bitmap
	- Stateful and non deterministic
		- Interrupts generate non-deterministic exections
		- So the fuzzer runs the program multiple times and identifies such basic blocks
		- Adds it to blacklist
		- This is ignored when updating the coverage map
	- Hypercalls
		- Accessible from ring3
		- So add custom hypercalls that can help in fuzzing
			- Eg: crash, ask for input
- KVM-PT
	- vCPU specific traces
		- MSR autoload feature lets you load MSRs on exit or entry
	- Continuous tracing
		- Uses ToPA
			- Table of physical address
			- Each address is associated with behavior on overflow
				- First -> interrupt
				- Second -> Stop tracing
					- But keep it large enough for this to never happen
		- On overflow it triggers and results in vm switch
		- Buffer is cleared and switched back to the VM
- QEMU-PT
	- Userspace application to interact with KVM-PT
	- When to start stop
	- Also does the decoding the trace to generate a AFL map
	- Our Intel PT software decoder acts like a just-in-time decoder, which means that code sections are only considered if they are executed according to the decoded trace data
		- ???
- Discussion
	- OS specific code
		- Not a necessity but improves fuzzing (cr3 value, custom process to test kernel)
	- Kernel JIT
		- Out of scope
		- But very interesting
		- Intel PT does not give all the instruction pointers and need the executable to decode
			- Becomes tricky
