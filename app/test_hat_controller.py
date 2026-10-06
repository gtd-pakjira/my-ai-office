from hat_controller import HatController


controller = HatController()

print("Start:", controller.current_hat.value)

print("Forward:", controller.move_forward().value)
print("Forward:", controller.move_forward().value)
print("Backward:", controller.move_backward().value)
print("Forward:", controller.move_forward().value)
print("Forward:", controller.move_forward().value)
print("Forward:", controller.move_forward().value)
print("Backward:", controller.move_backward().value)
print("Backward:", controller.move_backward().value)
print("Backward:", controller.move_backward().value)
print("Backward:", controller.move_backward().value)
print("Forward:", controller.move_forward().value)