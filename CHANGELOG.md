# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2024-03-07

### Added
- Initial release of InterAgent
- Core session management
- Task creation and management
- Messaging system between agents
- CLI tool (`interagent` command)
- Python API for programmatic use
- File-based protocol using `.interagent/` directory
- Support for Claude and Kimi collaboration
- Role-based collaboration (Principal, Delegate, Reviewer)
- Task status tracking (pending → assigned → in_progress → completed → approved)
- Message inbox system
- Example scripts (basic_workflow, parallel_workflow)
- CLI examples (bash and batch)
- Markdown templates for tasks and reviews
- Comprehensive documentation

### Features
- **Session Management**: Initialize and manage collaboration sessions
- **Task Delegation**: Create and assign tasks to agents
- **Status Tracking**: Track task progress through workflow
- **Messaging**: Send messages between agents
- **Inbox System**: Check pending messages
- **Git Integration**: All state stored in Git-trackable files
- **Capability-Based Routing**: Automatic task assignment based on agent strengths

---

## [Unreleased]

### Planned
- Web dashboard for visualizing collaboration
- Desktop notifications
- Slack/Discord integration
- Additional agent profiles
- Plugin system
- VS Code extension

---

## Release Notes Template

```
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements
```
