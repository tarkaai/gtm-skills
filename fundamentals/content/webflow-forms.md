---
name: webflow-forms
description: Create and configure forms in Webflow for lead capture, contact requests, and survey submissions with proper integrations.
tool: Webflow
difficulty: Setup
---

# Set Up Webflow Forms

### Step-by-step
1. In the Webflow Designer, add a Form Block to your page from the Add Elements panel.
2. Customize the form fields: add Input fields for name, email, company, and any qualifying questions.
3. Use field types appropriately: Email for email addresses, Tel for phone, Select for dropdowns, Textarea for open-ended responses.
4. Make critical fields required: at minimum, email should be required.
5. Style the form: customize colors, spacing, and the submit button to match your page design.
6. Set the form action: by default, Webflow stores submissions. You can also redirect to a thank-you page after submission.
7. Set up a thank-you page: create a page that confirms the submission and offers a next step (download, booking link, etc.).
8. Configure form notifications: in Webflow Settings > Forms, set up email notifications for new submissions.
9. Connect to external tools: use Webflow's integrations or webhooks to send form data to Attio, Loops, or n8n for processing.
10. Test the form: submit test entries, verify you receive notifications, and check that data flows to your connected tools.
