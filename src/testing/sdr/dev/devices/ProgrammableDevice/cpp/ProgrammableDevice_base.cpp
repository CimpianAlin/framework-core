
#include "ProgrammableDevice_base.h"

/*******************************************************************************************

    AUTO-GENERATED CODE. DO NOT MODIFY

    The following class functions are for the base class for the device class. To
    customize any of these functions, do not modify them here. Instead, overload them
    on the child class

******************************************************************************************/

ProgrammableDevice_base::ProgrammableDevice_base(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl) :
    ExecutableDevice_impl(devMgr_ior, id, lbl, sftwrPrfl),
    AggregateDevice_impl(),
    serviceThread(0)
{
    construct();
}

ProgrammableDevice_base::ProgrammableDevice_base(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, char *compDev) :
    ExecutableDevice_impl(devMgr_ior, id, lbl, sftwrPrfl, compDev),
    AggregateDevice_impl(),
    serviceThread(0)
{
    construct();
}

ProgrammableDevice_base::ProgrammableDevice_base(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities) :
    ExecutableDevice_impl(devMgr_ior, id, lbl, sftwrPrfl, capacities),
    AggregateDevice_impl(),
    serviceThread(0)
{
    construct();
}

ProgrammableDevice_base::ProgrammableDevice_base(char *devMgr_ior, char *id, char *lbl, char *sftwrPrfl, CF::Properties capacities, char *compDev) :
    ExecutableDevice_impl(devMgr_ior, id, lbl, sftwrPrfl, capacities, compDev),
    AggregateDevice_impl(),
    serviceThread(0)
{
    construct();
}

void ProgrammableDevice_base::construct()
{
    Resource_impl::_started = false;
    loadProperties();
    serviceThread = 0;
    
    PortableServer::ObjectId_var oid;
}

/*******************************************************************************************
    Framework-level functions
    These functions are generally called by the framework to perform housekeeping.
*******************************************************************************************/
void ProgrammableDevice_base::initialize() throw (CF::LifeCycle::InitializeError, CORBA::SystemException)
{
}

void ProgrammableDevice_base::start() throw (CORBA::SystemException, CF::Resource::StartError)
{
    boost::mutex::scoped_lock lock(serviceThreadLock);
    if (serviceThread == 0) {
        serviceThread = new ProcessThread<ProgrammableDevice_base>(this, 0.1);
        serviceThread->start();
    }
    
    if (!Resource_impl::started()) {
    	Resource_impl::start();
    }
}

void ProgrammableDevice_base::stop() throw (CORBA::SystemException, CF::Resource::StopError)
{
    boost::mutex::scoped_lock lock(serviceThreadLock);
    // release the child thread (if it exists)
    if (serviceThread != 0) {
        if (!serviceThread->release(2)) {
            throw CF::Resource::StopError(CF::CF_NOTSET, "Processing thread did not die");
        }
        serviceThread = 0;
    }
    
    if (Resource_impl::started()) {
    	Resource_impl::stop();
    }
}

void ProgrammableDevice_base::releaseObject() throw (CORBA::SystemException, CF::LifeCycle::ReleaseError)
{
    // This function clears the device running condition so main shuts down everything
    try {
        stop();
    } catch (CF::Resource::StopError& ex) {
        // TODO - this should probably be logged instead of ignored
    }

    // deactivate ports
    releaseInPorts();
    releaseOutPorts();


    ExecutableDevice_impl::releaseObject();
}

void ProgrammableDevice_base::loadProperties()
{
    addProperty(device_kind,
                "DCE:cdc5ee18-7ceb-4ae6-bf4c-31f983179b4d",
                "device_kind",
                "readonly",
                "",
                "eq",
                "allocation,configure");

    addProperty(device_model,
                "DCE:0f99b2e4-9903-4631-9846-ff349d18ecfb",
                "device_model",
                "readonly",
                "",
                "eq",
                "allocation,configure");

    addProperty(hw_load_statuses,
                "hw_load_statuses",
                "hw_load_statuses",
                "readwrite",
                "",
                "external",
                "configure");

    addProperty(hw_load_requests,
                "hw_load_requests",
                "hw_load_requests",
                "readwrite",
                "",
                "external",
                "configure");

}


