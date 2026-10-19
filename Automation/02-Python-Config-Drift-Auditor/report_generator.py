import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


class ReportGenerator:
    def __init__(self, template_dir='templates', output_dir='reports'):
        self.template_dir = template_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def html_report(self, audit_results):

        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('report_template.html')

        total_devices = len(audit_results)

        has_errors = any(
            a.get("status") == "ERROR" for a in audit_results
        )
        has_drift = any(
            a.get("drift_detected") is True
            for a in audit_results
        )
        total_drifts = sum(
            a.get("total_changes", 0)
            for a in audit_results
        )
        if has_errors:
            overall_status = "ERROR"
            status_class = "status-error"
            message = "Error Detected during Audit"
        elif has_drift:
            overall_status = "DRIFT DETECTED"
            status_class = "status-drift"
            message = "Configuration Drift Found"
        else:
            overall_status = "FULLY COMPLIANT"
            status_class = "status-compliant"
            message = "No Configuration Drift Found"

        html = template.render(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status=overall_status,
            status_class=status_class,
            message=message,
            total_devices=total_devices,
            total_drifts=total_drifts,
            devices=audit_results
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"compliance_report_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w") as f:
            f.write(html)

        print(f"\n Report Finished | {filepath}")
        return filepath
