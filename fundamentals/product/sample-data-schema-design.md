---
name: sample-data-schema-design
description: Design realistic sample data schemas that demonstrate product value for new user accounts
tool: Product Database / ORM
difficulty: Config
---

# Sample Data Schema Design

Design a sample data schema that pre-populates new user accounts with realistic, domain-appropriate data so users can explore product functionality without manual setup.

## When to Use

When building a sample data acceleration play. The schema defines what sample records to create, how they relate to each other, and what state each record should be in to demonstrate the product's core value proposition.

## Instructions

### 1. Identify the product's core objects

Query your product database schema or ORM models to list all user-facing entities. For each entity, determine:

- Is it a **primary object** (the thing users create and manage, e.g., projects, contacts, campaigns)?
- Is it a **supporting object** (enriches primary objects, e.g., tags, comments, attachments)?
- Is it a **system object** (configuration, settings — skip these for sample data)?

Focus sample data on primary objects and the supporting objects that make them look realistic.

### 2. Define the sample data graph

For each primary object, specify:

```json
{
  "entity": "project",
  "sample_count": 3,
  "states": ["completed", "in_progress", "not_started"],
  "supporting_objects": [
    { "entity": "task", "per_parent": 5, "states": ["done", "done", "in_progress", "todo", "todo"] },
    { "entity": "comment", "per_parent": 2, "content_type": "realistic_discussion" },
    { "entity": "attachment", "per_parent": 1, "content_type": "placeholder_document" }
  ],
  "relationships": [
    { "entity": "team_member", "type": "many_to_many", "count": 3 }
  ]
}
```

Rules for the graph:
- Include at least one object in each meaningful state (completed, in-progress, not-started) so users see the full lifecycle
- Use 3-5 primary objects — enough to feel populated, not so many it overwhelms
- Supporting objects should have realistic counts (a project with 200 tasks feels wrong; 5-10 feels right)
- Include at least one relationship that demonstrates collaboration (shared objects, assigned users)

### 3. Write realistic content

Sample data content must be:
- **Domain-appropriate**: If the product is a CRM, use realistic company names, deal amounts, and pipeline stages. If it is a project management tool, use realistic project names and task descriptions
- **Internally consistent**: Dates, statuses, and relationships must make logical sense (a completed task should have a completion date before today)
- **Demonstrative**: At least one sample record should showcase the product's unique differentiator — the feature that competitors lack
- **Non-generic**: "Acme Corp" and "Lorem ipsum" signal laziness. Use varied, plausible names and content

Use an LLM (Claude API via `anthropic-api-patterns`) to generate realistic content at scale. Prompt structure:

```
Generate {count} realistic {entity} records for a {product_type} product.
Each record needs: {field_list}.
Requirements:
- Varied industries and company sizes
- Realistic dates within the last 90 days
- At least one record should demonstrate {unique_feature}
- Output as JSON array
```

### 4. Define the schema as a seed file

Output the complete schema as a JSON seed file that your product's backend can consume:

```json
{
  "schema_version": "1.0",
  "product_type": "{your_product_type}",
  "entities": [
    {
      "entity": "project",
      "records": [
        {
          "id": "sample_project_1",
          "name": "Q1 Product Launch",
          "status": "completed",
          "created_at": "2026-01-15T10:00:00Z",
          "completed_at": "2026-03-01T16:30:00Z",
          "tasks": ["sample_task_1", "sample_task_2"],
          "_sample": true
        }
      ]
    }
  ],
  "metadata": {
    "created_by": "sample-data-seeding-drill",
    "persona": "{target_user_persona}",
    "demonstrates": ["{feature_1}", "{feature_2}"]
  }
}
```

Mark every sample record with `_sample: true` so the product can distinguish sample data from real user data and allow bulk deletion.

### 5. Validate the schema

Before deploying:
- Verify all foreign key references resolve (no orphaned relationships)
- Verify date sequences are logical (created_at < updated_at < completed_at)
- Verify enum values match the product's actual allowed values
- Verify required fields are populated
- Verify the total data volume stays small (under 50 records total across all entities)

## Output

A JSON seed file containing the complete sample data graph, ready for the `seed-data-injection` fundamental to deploy into user accounts.

## Error Handling

- If the product schema changes (new required fields, renamed entities), the seed file breaks. Pin the seed file to a schema version and validate on deployment.
- If sample data content becomes stale (references to outdated industry trends or tools), regenerate content quarterly using the LLM prompt.
