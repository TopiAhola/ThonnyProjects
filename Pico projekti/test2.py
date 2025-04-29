# def show_kubios_result(self):
#     header: str = "Kubios Result"
#     print(header)
#
#     if self.kubios_strings[0] != f"id: {self.id}":
#         self.kubios_strings = self.response_string(self.last_response)
#
#     elif self.kubios_strings[0] == f"id: {self.id}":
#         self.update_cursor(len(self.kubios_strings) - 5)
#         oled.fill(0)
#         oled.text("Kubios results:", 0, 0, 1)
#         n = 0
#         for line in self.kubios_strings[self.cursor_position: self.cursor_position + 5]:
#             oled.text(line, 0, 8 + 8 * n, 1)
#             n = n + 1
#         oled.show()
#
#         if button.get() or rtm_button.get() or return_button.get():
#             self.state = self.main_menu
#
#         time.sleep(self.cycle_time)
#     else:
#         print("Kubios string list error!")



kubios_strings = [f'LF_HF_power',
            f'stress_index',
            f'type',
            f'mean_hr_bpm',
            f'version',
            f'physiological_age',
            f'effective_time',
            f'readiness',
            f'pns_index',
            f'sdnn_ms',
            f'artefact_level',
            f'sd1_ms',
            f'effective_prc',
            f'sd2_ms']
cursor_position = 0
for line in kubios_strings[cursor_position : cursor_position + 5]:
    print(line)