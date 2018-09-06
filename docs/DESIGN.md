# Daedalus Design Documentation
Currently just notes on the system design, eventually this space will be used to describe the system to aid
in development and collaboration.

### System States
__CREATED__

The system has been created but no data has been supplied to train a surrogate

__TRAINING__

The system has been created, some number of datasets have been supplied, and the surrogate model 
is currently in the training process. 

New datasets can be added and predictions can be made on the currently supplied dataset, however 
requests for experimental desings to improve the surrogate via the 'adapt' REST calls will result in an error.

NOTE: For reproducibility of results and better handling of the system state for functionality; surrogates
could be versioned with each of the saved to disk and referenced by ID. The potential issue with this is that 
each surrogate takes up a relevant amount of space, and if a surrogate is being adapted a point at a time 
(or has simply been around for awhile and heavily used/adaped), could result is an excessive amount of storage
space being required.

NOTE: The state of 'TRAINING' might not be appropriate for all situations that would indicate the surrogate has
limited functionality at this time. Consider refactoring this to 'BUSY'

__READY__

The system and trained surrogate are not currently involved in any calculations and are free to be used.

__ERROR__

Something happening with the model or surrogate to put it in an error state and is unable to be 
used for basic functionality.

NOTE: Still need to identify when these error states could occur, and provide functionality to fix it. 

### Issues

Daedalus has a variety of functionality via the REST API that does not involve the creation of a persistent resource,
e.g. /adapt and /predict which has an API for interaction over the wire but not in a standard REST form of interaction
where a resource is created. Some research needs to be done to see what existing design patterns say about this 
concept and if each of these methods should actually create a persistent resource. If so, the web frontend and client
will need to be updated in order to view previous calls to these methods.

#### Scalability

Some potential bottlenecks for scaling the system

Surrogate Model Training/Analysis: The numerical calculations involved in the system functionality are likely
to compete with basic HTTP server resources. These calculations should be moved to a cluster and can be treated
like a thread pool with round-robin load balancing (at least until user priority levels are implemented). The only
thing the HTTP server needs to handle is setting the state of the system to busy is calculations are occuring/
going to occur that would affect functionality so the Redis or RabbitMQ piece can be shipped out. Stress testing should
be performed to evaluate if EC2 instances can be spooled up to handle load faster than surrogates would naturally be 
trained. Meta-models of train_time as f(n_dim, n_train) could be useful to determine if a new instance should be 
spun up or if it is better just to wait until a resource is available.

Surrogate Model Persistence: The serialized data for the surrogate model which is currently being saved as a file
can be quite large, as such they should not be saved on the HTTP server or database but still need to be 
accessed quickly. In essence these files represent the 'media' that a media server would handle, however, instead
of being served up directly to the user, they would be served to the system performing analysis that consumes and/or
updates the surrogate. This is a place where caching could be very helpful to pre-load the surrogate into memory and
make if available to active users. Something like memcached may be helpful here however most caching solutions
are designed to deal with simple key:value pairs and so a custom solution may be required.

Request Load: Since one of the use cases for Daedalus is for it to be utilized by automated systems, and given that
the current state of the system and associated surrogate are important for control flow, a large ammount of requests
are likely to be generated for even a small user based. Likely horizontal scaling would be the best approach by 
placing a load balancing system up front and having a cluster of HTTP servers to manage the load from each client.

Timeouts: Given that much of the functionality of Daedalus relies on numerical analysis, request timeouts are a real
concern. For example, a simple system/model is very fast to respond to a prediction request, however, for a very
complex model, it is possible that the analysis may take longer than standard HTTP request timeout times resulting
in an error (and an upset user). How can this be handled without turning every analysis request into a polling operation
to check the state of the operation which would only exacerbate system load issues. 

#### Users

Currently Daedalus does not have a concept of users. This will absolutely need to be implemented before deployment. 
Users should have multiple role levels

System Admin: Has total administrative abilities including being able to create/delete/update users. Monitor system
usage and statistics. Update/Delete systems, ex. clean out old surrogates that are no longer being used or transfer
ownership of these systems.

Group Admin: Had administrative abilities for systems associated with a group. Able to add/remove users,
update/delete systems. Able to update user roles related to that group.

Use Case: New employee comes on board. Sys admin gives them an account and assigns them to a group with 'READ'
access so they can view and predict on models. Users begins producing training data for the workgroup, so the Group 
Admin should then be able to give them 'WRITE' access to upload datasets that will be included in the training
data for the surrogate.

User: Can create/update systems they are associated with. Can be part of a group

Group: Systems can be associated with a group where all users associated with that group can update/use those systems. 

SSO: Some organizations that would want to use this system will want to integrate it with their current SSO system 
so that users don't have to log in to multiple utilities. Is there a way to handle SSO in general so that a 
customization will not need to be created for each of these organizations?

