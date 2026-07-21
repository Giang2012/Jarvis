from kernel.kernel import kernel

print("===== TEST KERNEL =====")

print("Status:", kernel.state.status)
print("Mode:", kernel.state.mode)
print("CPU:", kernel.state.cpu)
print("RAM:", kernel.state.ram)