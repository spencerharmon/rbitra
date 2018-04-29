# rbitra.io

#### Consensus Process Translator:
- Consensus Process -> Decision Engine
- Proposal -> Decision
- Friendly Amendment -> Modification
- Clarifying Question -> Q
- Response -> A
- Point of Information -> Info Item

#### Questions:
- Is git fast enough/can git or compatible clones be fast enough to support this? How does github et al do this?

tagline(s):
	Insight through collaboration
	make a decision
	make a decision to make a decision

## Summary:
rbitra is built with the belief that the version control software git is basically the best model for collaboration but that implementaions for use outside code devlopment are scarce or non-existant. As primarily a decision engine, rbitra extends the version control features of git by keeping a decision's repository that contains all of the modifications approved by the organization's policy.
rbitra is a python flask web application and REST api that uses git repositories as a foundation for a group decision-making platform. It is designed especially for grassroots and non-profit organizations, free software developers, and other communities or organizations who stand to benefit from a distributed decision-making process.
You can use rbitra for your organization to collaborate on and make decisions about:
 - emails sent from group mailbox aliases
 - organizational documents or templates
 - project planning
 - code changes

### Views
Decision views are represented as the contents of a file located at the head of a git repository or as the directory structure at the head of a git repository in cases where multiple files are involved in the decision. In the decision view, members with read-only permissions based on their role and the decision's policy may see all contents, questions, answers, info items, suggested modifications, and concerns for a decision. Members with read-write permission may also ask or answer questions, add info items, suggest modifications, or raise concerns.
statistics - view organizational statistics on things like approved decisions, blocking concerns, block overrides, member participation, decision creation, modification submission, et c.
Decision list - members (or unauthenticated users) can view lists of decisions for each scope their role allows them at least read access. Sorts and filters. All members can view or participate in public decisions. Members of organizations will have a list of decisions wit policy scope for their role for that organization. Top level list for each role "under" member's role in an organization. Looks like this:

- Public
- Hippie Cult
  - Inner Circle
  - Officer
  - Peon
- Python Programmers Inc
  - Developer
- Egalitarian Community Pantry

This list of lists illustrates that the member is associated with three organizations, Hippie Cult, Python Programmers, Inc, and Egalitarian Community Pantry. The public list has all decisions from any organization with a read-only or read-write policy for public members. The lists for each organization will show all decisions for the logged-in member's role within that organization (if applicable). Each item nested below the organization list is a list of items for roles at or below the member's role within that organization. This member is a member of the Inner Circle role of Hippie Cult. Officer and Peon are ancestors of the Inner Circle role. Each of these lists shows only decisions which are created by members with that role within the organization.
Likewise, for Python Programmmers Inc, the member may view all of the decisions for which they have permission in the organization (by selecting the list "python Programmers Inc") or only the decisions for their role, Developer. The Egalitarian Community Pantry organization does not have roles, and therefore no lists appear for the member's role nested under this organization.

- Decisions:
	- properties:
		- guid
		- title
		- author
		- description
		- policy (separate table)
		- plugin
		- plugin properties (separate table)

Decisions are ideas proposed by a member of an organization. Creating a decision allows members with roles allowed by the decision's policy to ask questions, provide information, propose modifications, share concerns, and support, oppose, or remain neutral on modifications or decisions.

### Concerns:
Concerns are an item of critique about a decision. These represent things that could be improved about a decision.
Any user with roles within the scope of a decisions policy may create a concern.

Any concern may be marked as a blocking concern. A decision cannot achive approval status (or enact approval behavior) as long as there is a blocking concern. This can be thought of like the Andon cord from the Lean approach.

Blocking concerns can be overridden according to the block_override_quorum set for an organization. This quorum is represented as a percentage, in decimal notation. When the number of block_overrides for a concern divided by the number of members participating in the decision (whose roles are in the scope of the decision's policy) exceeds the quorum, a concern's block is overriden.

Block overrides are generally considered less desireable than a modification that removes members' cause for concern. Too many block overrides may indicate a conflict in values within an organization.
Modifications can be suggested for concerns. Approval of a modification on a concern changes a concern to a resolved status. Members whose link to a concern has a blocking attribute must be among the approvers of a modification suggested for the concern or it cannot be approved.

It is considered very good practice to resolve blocking concerns this way.
Unresolved concerns always remain visible on a decision.

It is not considered a problem to have unresolved concerns on decisions, even if they're approved. These can be considered as notes or suggestions for future improvement.

### Modifications:
Modifications are suggestions to alter the contents of a decision. The approval of a modification (and therefore the modification of the contents of a decision) takes place when the modification quorum is reached.

### Quora:
Different aspects of the decision engine depend on quora. These are mutable properties of the organization.

- Decision - must be met to approve a decision
- Modification  - must be met to apply a modification to a decision
- Block override - must be met to override a blocking concern
- Admin - must be met to approve admin decisions

### Roles and Policies
- Roles are associated with an organization to link to members to policies.
- Policies link decisions to roles.
- A policy has one of two types: observe (read-only) or participate (read-write).
- There are two default roles, public, and organization
- Public - any member from any organization (Read only for unauthenticated users)
- Organization - any member of this organization
- Organizations may define a custom internal role structure. a role's parent will always have read/write permission for all of its policies.

Default roles represent a separate, predefined (by the relationship of members to organizations) higherarchy for decisions. the custom organization refines roles.

Organizations may define custom roles. An organization must have at least one role without a parent. Subsequent roles may optionally have one parent.

Members may create policies for decisions that they alter, either read-only or read-write, for roles at or below their own role.

Only members of a role with no parent (a top-level role) or members of organizations with no custom roles may participate in admin decisions for the oganization. Organizations that do not define custom roles allow all members of their organization to make admin decisions.

Admin decisions include decisions to add or change policies for another decision (e.g., to make it read only to the public or read write to the organization), or modifying attributes of the organization such as name, any of the quora, or default decision roles. There must be one or more members who may make admin decisions.

Policies for the public or organization role may only be created or modified after a decision is created by reaching an admin quorum to creat the attribute. An admin decision can also change the default behavior of default policies for the organization's decisions (including policies for the public or organization role).
	All decisions must have at least one policy with read-write permission for a role.

- Plugins
	- Email:
	  - create and send emails with a team through rbitra
	  - connects to mailbox on remote mailserver to send emails on behalf of the mailbox
	  - navigate inbox to create replies as decisions
	  -other mailbox management like folder creation, mailbox rules, deletion, marking as spam, et c. is best handled in other applications, though support for making these decisions should be supported in the future
	- Documents:
		- default plugin

	- project
		- the project plugin is, again, backed by a git repository.

		- a project is roughly defined as a representation of things for members to do and who will do them
		- the only thing that's really special about an action is that members are given the namedInAction role by default which gives them permission to participate in the decision
		- all members who are named in t
	- GIT
		- default plugin
		- integration mechanisms:
		  - collaborators file - members can specify collaborators who are stored in this file which is referenced along with the member's git user for attributing modifications.
		  - Decisions are modeled as repositories, with the decision repository's head representing the current status.
		  - A clone of each repository is created for each member who's role places it in the decision's scope
		  - Members may modify this using built-in collaboration software or clone the repository for local access.
		  - Members may submit modifications. A modification is represented as the commit at the head of a member's cloned repository on the rbitra server.
		  - When a modification is accepted, the decision repository merges the modification commit.
### Collaboration:
Members editing modification through the rbitra portal can choose to turn on collaboration which will allow other members to edit files simultaneously on their repository within the rbitra portal.
	Members can choose to add collaborators to a modification. This can be done through the rbitra portal or by creating a .rbitra_collaborators JSON file in the git repository

ORM/DB

	organization
	    id (primary)
		name
		server_key (foreign, default: localhost)

	role
	    id (primary)
		organization_key (foreign)
		name

	member_role
		role_key(foreign)
		member_key (foreign)

	policy
	    id (primary)
		organization_key (foreign)
		policy_type #RO or RW
		name

	policy_role
		policy_key (foreign)
		role_key (foreign)

	decision_policy
		decision_key (foreign)
		policy_key (foreign)

	decision
		title
		organization_key (foreign)

	modification
		commit_id
		repo_uri
		decision_key
		concern_key (can be none)

	concern
		decision_key (foreign)
		author_member_key (foreign)
		resolved_bool
		bool_block #blocking concern: true or false
		description

	concern_block_override
		concern_key
		member_key

	concern_member
		concern_key (foreign)
		member_key (foreign)

	member_organization
		organization_key (foreign)
		member_key (foreign)

	member
	    id (primary)
		name
		server_key (foreign, default: localhost)

	server
		fqdn
		port (443)



Always do API calls, even for local information. This makes the application distributed by default. Local objects have a server value which represents the localhost so that requests will be made over loopback address. Webserver must listen on loopback.
The idea is that larger organizations will host their own members and orgs where they need a high degree of integration with their existing business processes. E.g.: they would like to use rbitra to approve company purchasing and automate their purchasing process once approval is achieved. With a local instance of rbitra,
