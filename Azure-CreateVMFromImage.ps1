<#
	.SYNOPSIS

	Create a virtual machine in Azure from a saved image.
	.DESCRIPTION

	This function will create a virtual machine from the specified image. It will also create a virtual network with subnets, a disk, and set up the operating system for the new machine. If the specified resource group or virtual network does not exist, the user will be asked if they wish to create those objects. By default, the virtual network will be created with two subnets: 'front-end' and 'back-end'. In addition, the 'front-end' subnet will have a security group allowing remote desktop connection (unless specified otherwise). REQUIRES AzureRm Library (https://docs.microsoft.com/en-us/powershell/azure/install-azurerm-ps?view=azurermps-5.1.1)
	
	.PARAMETER SubscriptionId

	Subscription that contains the specified image and where the new virtual machine will be created.
	.PARAMETER VirtualMachineName

	The name of the new virtual machine.
	.PARAMETER ResourceGroupName

	The resource gorup that the new virtual machine will be created in
	.PARAMETER Location

	The location that the new virtual machine will be located in.
	.PARAMETER ImageName

	The name of the image that will be used
	.PARAMETER ImageResourceGroupName

	The resource name that the specified image is located in.
	.PARAMETER StorageType

	The type of disk storage the new virtual machine will have. Default: 'StandardLRS'; Additional Info: 'https://docs.microsoft.com/en-us/azure/storage/common/storage-introduction'
	.PARAMETER VirtualNetworkName

	The name of the existing/new virtual network for the new virtual machine. Default: 'VN_$ResourceGroupName'
	.PARAMETER VirtualMachineSize

	The size of the new virtual machine. Default: 'Standard_B1S'; Additional Info: 'https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-memory'
	.PARAMETER Confirm

	If this flag is specified, the user will not be prompted to confirm the creation of a new virtual network or resource group if the specified entities can not be found.
	Instead, they will be automatically created. Also, the function will not wait for the virtual machine to be successfully updated and started, as this can take up to 30min.
	Once the virtual machine is created, the function will exit.
	.PARAMETER Linux

	If this flag is specified, the operating system of the new virtual machine will be Linux.
	.PARAMETER DoNotCreateSecurityGroups

	If this flag is specified, the 'front-end' subnet will not have a security group. 
	
	.EXAMPLE
	Azure-CreateVMFromImage.ps1 -SubscriptionId "00000000-0000-0000-0000-000000000000" -VirtualMachineName "Noobie" -ResourceGroupName "NewGroup" -Location "EastUS" -ImageName "MyImage" -ImageResourceGroupName "MyImageGroup"
	
	.EXAMPLE	
	Azure-CreateVMFromImage.ps1 -SubscriptionId "00000000-0000-0000-0000-000000000000" -VirtualMachineName "Beefy" -ResourceGroupName "MooGroup" -Location "CentralUS" -ImageName "MyImage" -ImageResourceGroupName "MyImageGroup" -StorageType "PremiumLRS" -VirtualNetworkName "Spyder" -VirtualMachineSize "Standard_D13" -Confirm -Linux -DoNotCreateSecurityGroups
#>

param(
 [Parameter(Mandatory=$True)]
 [string]
 $SubscriptionId,

 [Parameter(Mandatory=$True)]
 [string]
 $VirtualMachineName,
 
 [Parameter(Mandatory=$True)]
 [string]
 $ResourceGroupName,
 
 [string]
 [Parameter(Mandatory=$True)]
 $Location,
 
 [string]
 [Parameter(Mandatory=$True)]
 $ImageName, 
 
 [string]
 [Parameter(Mandatory=$True)]
 $ImageResourceGroupName, 
 
 [string]
 $StorageType,

 [string]
 $VirtualNetworkName,
 
 [string]
 $VirtualMachineSize,
 
 [switch]
 $Confirm = $false,
 
 [switch]
 $Linux = $false,
 
 [switch]
 $DoNotCreateSecurityGroups
)

Write-Host "Importing AzureRM..."
Import-Module AzureRM

$message  = ""
$question = ""
$choices = New-Object Collections.ObjectModel.Collection[Management.Automation.Host.ChoiceDescription]
$choices.Add((New-Object Management.Automation.Host.ChoiceDescription -ArgumentList '&Yes'))
$choices.Add((New-Object Management.Automation.Host.ChoiceDescription -ArgumentList '&No'))

$ErrorActionPreference = "SilentlyContinue"

$temp = Get-AzureRmSubscription
$ErrorActionPreference = "Stop"

if(!$temp) {
	Write-Host "Gathering Credentials..." -NoNewLine
	$temp = Login-AzureRmAccount
	Write-Host "Success!"
}
 
Write-Host "Selecting designated subscription"
#Set the context to the subscription Id where Managed Disk will be created
$temp = Select-AzureRmSubscription -SubscriptionId $SubscriptionId

if(-Not($UserName) -or -Not($Password)) {
	$UserName = "User"
	$Password = ConvertTo-SecureString "Secret123" -AsPlainText -Force 
	Write-Host "Set the VM username to '$UserName' and password to 'Secret123'"
}

if(!((Get-AzureRmResourceGroup | Select ResourceGroupName) -Match $ResourceGroupName)) {
	if(-Not($Confirm)) {
		$message = "Can not find resource group with name '$ResourceGroupName'"
		$question = "Do you want to create this resource group?"
		$decision = $Host.UI.PromptForChoice($message, $question, $choices, 1)
		if ($decision -eq 0) {
			Write-Host "Creating new resource group... " -NoNewLine
		} else {
			Write-Host 'Exiting'
			return
		}
	} else {
		Write-Host "Creating a resource group with name '$ResourceGroupName'" -NoNewLine
	}
	$temp = New-AzureRmResourceGroup -Name $ResourceGroupName -Location $Location
	Write-Host "Success!"
}

if(-Not($StorageType)) {
	$StorageType = "StandardLRS"
	Write-Host "Set the account storage type to '$StorageType'"
}

if(-Not($VirtualMachineSize)) {
	$VirtualMachineSize = 'Standard_B1S'
	Write-Host "Set the virtual machine size to '$VirtualMachineSize'"
}

#Provide the name of an existing virtual network where virtual machine will be created
if(-Not($VirtualNetworkName)) {
	$VirtualNetworkName = "VN_$ResourceGroupName"
	Write-Host "Set the virtual network name to '$VirtualNetworkName'"
} 

# Determining if the virtual network already exists
$temp = Get-AzureRmVirtualNetwork -ResourceGroupName $ResourceGroupName -Name $VirtualNetworkName -ErrorAction SilentlyContinue
if(-Not($temp)){	
	if(-Not($Confirm)) {
		$message = "Can not find virtual network with name '$VirtualNetworkName' in resource group '$ResourceGroupName'"
		$question = "Do you want to create this virtual network?"
		$decision = $Host.UI.PromptForChoice($message, $question, $choices, 1)
		if ($decision -eq 0) {
			Write-Host "Creating new virtual network (this can take a minute)... " -NoNewLine
		} else {
			Write-Host 'Exiting'
			return
		}
	} else {
		Write-Host "Creating a virtual network with name '$VirtualNetworkName' in resource group '$ResourceGroupName' (this can take a minute)... " -NoNewLine
	}
	
	
	if(!$DoNotCreateSecurityGroups) {
		$rule1 = New-AzureRmNetworkSecurityRuleConfig -Name rdp-rule -Description "Allow RDP" -Access Allow -Protocol Tcp -Direction Inbound -Priority 1000 -SourceAddressPrefix * -SourcePortRange * -DestinationAddressPrefix * -DestinationPortRange 3389 -WarningAction silentlyContinue
		$nsgName = $VirtualMachineName.ToLower()+"_nsg"
		$nsg = New-AzureRmNetworkSecurityGroup -ResourceGroupName $ResourceGroupName -Location $Location -Name $nsgName -SecurityRules $rule1 -WarningAction silentlyContinue
		$frontendSubnet = New-AzureRmVirtualNetworkSubnetConfig -Name "frontEnd" -AddressPrefix "10.0.1.0/24" -NetworkSecurityGroup $nsg -WarningAction silentlyContinue
		$backendSubnet  = New-AzureRmVirtualNetworkSubnetConfig -Name "backEnd"  -AddressPrefix "10.0.2.0/24" -WarningAction silentlyContinue	
		$temp = New-AzureRmVirtualNetwork -Name $VirtualNetworkName -ResourceGroupName $ResourceGroupName -Location $Location -AddressPrefix "10.0.0.0/16" -Subnet $frontendSubnet,$backendSubnet -WarningAction silentlyContinue		
	}
	else {
		$frontendSubnet = New-AzureRmVirtualNetworkSubnetConfig -Name "frontEnd" -AddressPrefix "10.0.1.0/24"  -WarningAction silentlyContinue	
		$backendSubnet  = New-AzureRmVirtualNetworkSubnetConfig -Name "backEnd"  -AddressPrefix "10.0.2.0/24" -WarningAction silentlyContinue			
		$temp = New-AzureRmVirtualNetwork -Name $VirtualNetworkName -ResourceGroupName $ResourceGroupName -Location $Location -AddressPrefix "10.0.0.0/16" -Subnet $frontendSubnet,$backendSubnet -WarningAction silentlyContinue
	}	
	Write-Host "Success!"
}
 
Write-Host "Configuring the VM: " -NoNewLine
$VirtualMachine = New-AzureRmVMConfig -VMName $VirtualMachineName -VMSize $VirtualMachineSize

Write-Host "specifying the OS" -NoNewLine
$Credential = New-Object System.Management.Automation.PSCredential ($UserName, $Password); 
if($Linux) { 
	$VirtualMachine = Set-AzureRmVMOperatingSystem -VM $VirtualMachine -Linux -ComputerName $VirtualMachineName -ProvisionVMAgent -EnableAutoUpdate -Credential $Credential
} else {
	$VirtualMachine = Set-AzureRmVMOperatingSystem -VM $VirtualMachine -Windows -ComputerName $VirtualMachineName -ProvisionVMAgent -EnableAutoUpdate -Credential $Credential
}

Write-Host ", setting the source image" -NoNewLine
$image = Get-AzureRmImage -ImageName $ImageName -ResourceGroupName $ImageResourceGroupName
$VirtualMachine = Set-AzureRmVMSourceImage -VM $VirtualMachine -Id $image.Id

Write-Host ", creating an IP address" -NoNewLine
#Create a public IP for the VM  
$publicIp = New-AzureRmPublicIpAddress -Name ($VirtualMachineName.ToLower()+'_ip') -ResourceGroupName $ResourceGroupName -Location $Location -AllocationMethod Dynamic -WarningAction silentlyContinue

#Get the virtual network where virtual machine will be hosted
$vnet = Get-AzureRmVirtualNetwork -Name $VirtualNetworkName -ResourceGroupName $ResourceGroupName

Write-Host ", creating the Network Interface" -NoNewLine
# Create NIC in the first subnet of the virtual network 
$nic = New-AzureRmNetworkInterface -Name ($VirtualMachineName.ToLower()+'_nic') -ResourceGroupName $ResourceGroupName -Location $Location -SubnetId $vnet.Subnets[0].Id -PublicIpAddressId $publicIp.Id -WarningAction silentlyContinue
Write-Host "... Success!"

Write-Host "Creating the VM... "
$VirtualMachine = Add-AzureRmVMNetworkInterface -VM $VirtualMachine -Id $nic.Id

#Create the virtual machine with Managed Disk
$temp = New-AzureRmVM -VM $VirtualMachine -ResourceGroupName $ResourceGroupName -Location $Location -AsJob -WarningAction silentlyContinue

$state = ""
do{
	Start-Sleep -s 1
	$newState = (Get-AzureRmVM -ResourceGroupName $ResourceGroupName -Name $VirtualMachineName).ProvisioningState -ErrorAction silentlyContinue
	if(-Not($newState -eq $state))
	{
		if($state -eq "")
		{
			Write-Host $newState -NoNewLine
		}
		else
		{
			Write-Host " -->  $newState" -NoNewLine
		}
	}
	$state = $newState
} while(-Not($state -eq "Succeeded") -and -Not($state -eq "Failed"))

if(-Not($Confirm)) {
	$message = "Virtual machines can take up to 30min to configure and update"
	$question = "Do you want to skip waiting for the VM?"
	$decision = $Host.UI.PromptForChoice($message, $question, $choices, 1)
} 

Write-Host ""
if($state -eq "Succeeded" -and (-Not($Confirm) -and $decision -eq 1))
{	
	Write-Host "Checking for updates: " -NoNewLine	
	$state = ""
	do{
		Start-Sleep -s 5
		$newState = (Get-AzureRmVM -ResourceGroupName $ResourceGroupName -Name $VirtualMachineName).ProvisioningState
		if(-Not($newState -eq $state))
		{
			Write-Host $newState -NoNewLine
		} else 
		{
			Write-Host "." -NoNewLine
		}
		$state = $newState
	} while(-Not($state -eq "Succeeded") -and -Not($state -eq "Failed"))
	Write-Host ""
	#Write-Host "Done!"
	Write-Host "New VM, '$VirtualMachineName', created and configured in resource group '$ResourceGroupName' and ip address '$ip. Machine is currently running. You will need to restart the VM to kick off selenium or remote into it and start it manually. "	
}
elseif ($Confirm -or $decision -eq 0) {
	Write-Host "Skipping update checks."
	Write-Host "New VM, '$VirtualMachineName', created in resource group '$ResourceGroupName' and ip address '$ip. Machine is currently running. "
}
else{
	Write-Host "Failed to create the new VM, '$VirtualMachineName', in resource group '$ResourceGroupName'. Please check the status in the Portal"
}
Write-Host "Fin"