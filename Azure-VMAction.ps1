<#
	.SYNOPSIS

	Start or stop one or many virtual machines in Azure.
	.DESCRIPTION

	This function starts or stops the specied virtual machine(s) in the designated subscription. This is not location or resource group specific. Therefore, all virtual machines that match the specified names will have the specified action performed. REQUIRES AzureRm Library (https://docs.microsoft.com/en-us/powershell/azure/install-azurerm-ps?view=azurermps-5.1.1)
	
	.PARAMETER SubscriptionId

	Subscription that contains the specified VMs.
	.PARAMETER VMName

	The name of the vm the action will be performed on
	.PARAMETER VMNames

	The names of the virtual machines that the action will be performed on
	.PARAMETER Start

	If this flag is specified, the designated virtual machine(s) will be started
	.PARAMETER Stop

	If this flag is specified, the designated virtual machine(s) will be stopped
	.PARAMETER Wait

	If this flag is specified, the function will wait for the specified action to be fully completed.
	.PARAMETER ContinueOnActionFailure

	If this flag is specified, the function will continue to apply the action to other virtual machines even if it fails on one of the specified machines.
	.EXAMPLE
	Azure-VMAction.ps1 -SubscriptionId "00000000-0000-0000-0000-000000000000" -VMName "C3P0" -Stop -ContinueOnActionFailure
	.EXAMPLE	
	Azure-VMAction.ps1 -SubscriptionId "00000000-0000-0000-0000-000000000000" -VMNames "C3P0", "R2D2", "Wallie", "Cortana" -Start -Wait
#>

param(
 [Parameter(Mandatory=$True)]
 [string]
 $SubscriptionId,
 
 [string]
 $VMName,
 
 [String[]]
 $VMNames,
 
 [switch]
 $Stop,
 
 [switch]
 $Start,
 
 [switch]
 $Wait,
 
 [switch]
 $ContinueOnActionFailure
)
 
if((!$VMName -and !$VMNames) -or ($VMName -and $VMNames)) {
	$Name_Error = [string]"Failed to specify a VM, multiple VMs, or have specified both."
    Write-Error $Name_Error
	return
}

if((!$Start -and !$Stop) -or ($Start -and $Stop)) {
	$message  = "You have failed to select an action or have selected too many actions, for your VM, '$VMName'"
	$question = "Please select one below"
	$choices = New-Object Collections.ObjectModel.Collection[Management.Automation.Host.ChoiceDescription]
	$choices.Add((New-Object Management.Automation.Host.ChoiceDescription -ArgumentList '&Start'))
	$choices.Add((New-Object Management.Automation.Host.ChoiceDescription -ArgumentList 'Sto&p'))
	$choices.Add((New-Object Management.Automation.Host.ChoiceDescription -ArgumentList '&Cancel'))
	$decision = $Host.UI.PromptForChoice($message, $question, $choices, 2)
	switch ($decision)
    {
        0 {
			"'Start' selected."
			$Start = $true
		}
        1 {
			"'Stop' selected."
			$Stop = $true
		}
		2 {
			"Action canceled."
			return
		}
    }

}

Write-Host "Importing AzureRM..."
Import-Module AzureRM

$ErrorActionPreference = "SilentlyContinue"

$temp = Get-AzureRmSubscription
$ErrorActionPreference = "Stop"

if(!$temp) {
	Write-Host "Gathering Credentials..." -NoNewLine
	$temp = Login-AzureRmAccount
	Write-Host "Success!"
}

$temp = Select-AzureRmSubscription -SubscriptionId $SubscriptionId

if($VMName) {
	[string[]]$VMNames = $VMName
}

$availableVMs = Get-AzureRmVM
$selectedVMs = @()
foreach($vm in $availableVMs) { 
	if($VMNames -contains $vm.Name) { 
		$selectedVMs += $vm 
	} 
}

foreach ($item in $selectedVMs) {
	$VMName = $item.Name
	$ResourceGroupName = $item.ResourceGroupName
	
	$vm = Get-AzureRmVM -Name $VMName -ResourceGroupName $ResourceGroupName
	
	Write-Host "-------------------$VMName---------------------"
	
	if($Stop) {
		Write-Host "Stopping VM... " -NoNewLine
		if($Wait) {
			$r = Stop-AzureRmVM -Id $vm.Id -Name $vm.Name -Force
		} else {
			$r = Stop-AzureRmVM -Id $vm.Id -Name $vm.Name -AsJob -Force
		}
	} else {
		Write-Host "Starting VM... " -NoNewLine
		if($Wait) {
			$r = Start-AzureRmVM -Id $vm.Id -Name $vm.Name
		} else {
			$r = Start-AzureRmVM -Id $vm.Id -Name $vm.Name -AsJob
		}
	}

	$url = "https://portal.azure.com/#resource" + $vm.Id + "/"

	if(!$Wait) {
		Write-Host "Sucessfully requested action for VM. Check the status of the VM in the portal for more details ("$url")."
	}
	elseif($r){
		Write-Host "Sucessfully performed action for VM ("$url")."
	} else {
		Write-Host "Failure. See the Vm's activity log for more details ("$url"/eventlogs)."
		if(!$ContinueOnActionFailure) {
			break
		}
	}
	
	
}

Write-Host "--------------------------------------------------------"

Write-Host "Fin"